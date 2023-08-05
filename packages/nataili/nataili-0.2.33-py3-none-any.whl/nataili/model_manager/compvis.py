"""
This file is part of nataili ("Homepage" = "https://github.com/Sygil-Dev/nataili").

Copyright 2022 hlky and Sygil-Dev
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
import os
import time
from pathlib import Path

import torch
from omegaconf import OmegaConf
from torch import nn

from ldm2.util import instantiate_from_config
from nataili.cache import get_cache_directory
from nataili.model_manager.base import BaseModelManager
from nataili.util.logger import logger
from nataili.util.voodoo import push_model_to_plasma


class CompVisModelManager(BaseModelManager):
    def __init__(self, download_reference=True, custom_path="models/custom"):
        super().__init__()
        self.download_reference = download_reference
        self.path = f"{get_cache_directory()}/compvis"
        self.custom_path = custom_path
        self.models_db_name = "stable_diffusion"
        self.models_path = self.pkg / f"{self.models_db_name}.json"
        self.remote_db = (
            f"https://raw.githubusercontent.com/Sygil-Dev/nataili-model-reference/main/{self.models_db_name}.json"
        )
        self.init()

    def load(
        self,
        model_name: str,
        half_precision=True,
        gpu_id=0,
        cpu_only=False,
        voodoo=False,
    ):
        """
        model_name: str. Name of the model to load. See available_models for a list of available models.
        half_precision: bool. If True, the model will be loaded in half precision.
        gpu_id: int. The id of the gpu to use. If the gpu is not available, the model will be loaded on the cpu.
        cpu_only: bool. If True, the model will be loaded on the cpu. If True, half_precision will be set to False.
        voodoo: bool. Voodoo (Ray)
        """
        if model_name not in self.models:
            logger.error(f"{model_name} not found")
            return False
        if model_name not in self.available_models:
            logger.error(f"{model_name} not available")
            self.download_model(model_name)
            logger.init_ok(f"{model_name}", status="Downloaded")
        if model_name not in self.loaded_models:
            if not self.cuda_available:
                cpu_only = True
                voodoo = False
            tic = time.time()
            logger.init(f"{model_name}", status="Loading")
            self.loaded_models[model_name] = self.load_compvis(
                model_name,
                half_precision=half_precision,
                gpu_id=gpu_id,
                cpu_only=cpu_only,
                voodoo=voodoo,
            )
            toc = time.time()
            logger.init_ok(f"{model_name}: {round(toc-tic,2)} seconds", status="Loaded")
            return True

    def load_model_from_config(self, model_path="", config_path="", map_location="cpu"):
        config = OmegaConf.load(config_path)
        pl_sd = torch.load(model_path, map_location=map_location)
        if "global_step" in pl_sd:
            logger.info(f"Global Step: {pl_sd['global_step']}")
        sd = pl_sd["state_dict"] if "state_dict" in pl_sd else pl_sd
        model = instantiate_from_config(config.model)
        m, u = model.load_state_dict(sd, strict=False)
        model = model.eval()
        for m in model.modules():
            if isinstance(m, (nn.Conv2d, nn.ConvTranspose2d)):
                m._orig_padding_mode = m.padding_mode
        del pl_sd, sd, m, u
        return model

    def load_custom(self, ckpt_path, config_path, model_name=None, replace=False):
        if not os.path.isfile(ckpt_path):
            logger.error(f"{ckpt_path} not found")
            return
        if not os.path.isfile(config_path):
            logger.error(f"{config_path} not found")
            return
        if not ckpt_path.endswith(".ckpt"):
            logger.error(f"{ckpt_path} is not a valid checkpoint file")
            return
        if not config_path.endswith(".yaml"):
            logger.error(f"{config_path} is not a valid config file")
            return
        if model_name is None:
            model_name = os.path.basename(ckpt_path).replace(".ckpt", "")
        if model_name not in self.models or replace:
            self.models[model_name] = {
                "name": model_name,
                "type": "ckpt",
                "description": f"custom model {model_name}",
                "config": {
                    "files": [
                        {"path": f"{self.custom_path}/{model_name}.ckpt"},
                        {"path": f"{self.custom_path}/{model_name}.yaml"},
                    ]
                },
                "available": True,
            }
            self.available_models.append(model_name)

    def load_available_models_from_custom(self, replace=False):
        # ckpt files and matching config yaml files
        for file in os.listdir(self.custom_path):
            if file.endswith(".ckpt"):
                ckpt_path = f"{self.custom_path}/{file}"
                config_path = ckpt_path.replace(".ckpt", ".yaml")
                self.load_custom(
                    ckpt_path,
                    config_path,
                    replace=replace,
                )

    def load_compvis(
        self,
        model_name,
        half_precision=True,
        gpu_id=0,
        cpu_only=False,
        voodoo=False,
    ):
        ckpt_path = self.get_model_files(model_name)[0]["path"]
        ckpt_path = f"{self.path}/{ckpt_path}"
        config_path = self.get_model_files(model_name)[1]["path"]
        config_path = f"{self.pkg}/{config_path}"
        if cpu_only:
            device = torch.device("cpu")
            half_precision = False
        else:
            device = torch.device(f"cuda:{gpu_id}" if self.cuda_available else "cpu")
        logger.debug(f"Loading model {model_name} on {device}")
        logger.debug(f"Model path: {ckpt_path}")
        model = self.load_model_from_config(model_path=ckpt_path, config_path=config_path)
        model = model.half() if half_precision else model
        if voodoo:
            logger.debug(f"Doing voodoo on {model_name}")
            model = push_model_to_plasma(model) if isinstance(model, torch.nn.Module) else model
        else:
            model = model.to(device)
        return {"model": model, "device": device, "half_precision": half_precision}

    def check_model_available(self, model_name):
        if model_name not in self.models:
            return False
        return self.check_file_available(self.get_model_files(model_name)[0]["path"])
