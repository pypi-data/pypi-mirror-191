from diffusers import StableDiffusionPipeline
from diffusers.utils.import_utils import is_xformers_available
from .restoration import RealESRGAN, GFPGAN

from flask_socketio import SocketIO

import torch
import numpy as np
from .utils import auto_device

from threading import Event
from platform import system
import random
import eventlet

import sys
import gc

from typing import Literal


class StopRequestedException(Exception):
    pass


class OsmosisModel:
    type: Literal["diffusers"] | Literal["coreml"] | None
    name: str | None
    sio: SocketIO | None

    diffusers_model: StableDiffusionPipeline | None

    esrgan: RealESRGAN | None
    gfpgan: GFPGAN | None

    def __init__(self, sio: SocketIO):
        self.type = None
        self.name = None
        self.diffusers_model = None
        self.sio = sio

        self.stop_requested = Event()

        @self.sio.on("stop")
        def stop():
            self.stop_requested.set()

    def load_diffusers(self, model_id: str, revision: str = "main"):
        self.type = "diffusers"
        self.name = model_id

        self.diffusers_model = None
        gc.collect()

        self.diffusers_model = StableDiffusionPipeline.from_pretrained(
            model_id,
            revision=revision,
            safety_checker=None,
            torch_dtype=torch.float32,
        )

        if torch.cuda.is_available():
            self.diffusers_model.enable_sequential_cpu_offload()
        if is_xformers_available():
            self.diffusers_model.enable_xformers_memory_efficient_attention()
        else:
            self.diffusers_model.enable_attention_slicing()

        self.diffusers_model.to(auto_device())

        if system() == "Darwin":
            _ = self.diffusers_model("noop", num_inference_steps=1)

    def check_if_stop(self):
        if self.stop_requested.is_set():
            raise StopRequestedException()

    def txt2img(self, data: dict):
        if self.type == None:
            return

        prompt = data["prompt"]
        negative_prompt = data.get("negative_prompt", None)
        steps = data.get("steps", 30)
        seed = data.get("seed", -1)
        width = data.get("width", 512)
        height = data.get("height", 512)

        upscale = data.get("upscale", -1)
        face_restoration = data.get("face_restoration", None)

        if not prompt:
            raise TypeError("No prompt provided!")

        if seed < 0:
            seed = random.randrange(0, np.iinfo(np.uint32).max)

        try:
            self.stop_requested.clear()
            if self.type == "diffusers":

                def diffusers_callback(
                    step: int, timestep: int, latents: torch.FloatTensor
                ):
                    self.check_if_stop()
                    self.sio.emit(
                        "txt2img:progress", {"type": "main", "data": [step, steps]}
                    )
                    eventlet.sleep(0)

                generator = torch.Generator(
                    device="cuda" if torch.cuda.is_available() else "cpu"
                ).manual_seed(seed)

                self.check_if_stop()

                output = self.diffusers_model(
                    prompt=prompt,
                    width=width,
                    height=height,
                    num_inference_steps=steps,
                    negative_prompt=negative_prompt,
                    callback_steps=1,
                    callback=diffusers_callback,
                    generator=generator,
                ).images[0]

                self.check_if_stop()
            else:
                raise NotImplementedError()

            if upscale > -1 or face_restoration:
                self.sio.emit("txt2img:progress", {"type": "postprocessing"})
                eventlet.sleep(0)

            self.check_if_stop()

            if upscale > -1:
                self.esrgan = RealESRGAN()
                output = self.esrgan.upscale(output, upscale)
                self.esrgan = None

            self.check_if_stop()

            if face_restoration:
                self.gfpgan = GFPGAN()
                output = self.gfpgan.restore(output, face_restoration)
                self.gfpgan = None

            gc.collect()

            metadata = {
                "model": "stable diffusion",
                "model_weights": self.name,
                "model_hash": None,
                "app_id": "ryanccn/osmosis",
                "app_version": "0.0.1",
                "image": {
                    "prompt": [
                        {
                            "prompt": prompt,
                            "weight": 1.0,
                        }
                    ],
                    "steps": steps,
                    "cfg_scale": 7.5,
                    "threshold": 0,
                    "perlin": 0,
                    "height": height,
                    "width": width,
                    "seed": seed,
                    "seamless": False,
                    "hires_fix": False,
                    "type": "txt2img",
                    "postprocessing": [],
                    "sampler": "k_euler_a",
                    "variations": [],
                },
            }

            if upscale:
                metadata["image"]["postprocessing"].append(
                    {"type": "esrgan", "scale": upscale, "strength": 0.75}
                )
            if face_restoration:
                metadata["image"]["postprocessing"].append(
                    {"type": "gfpgan", "strength": 0.5}
                )

            return {"image": output, "metadata": metadata}
        except StopRequestedException:
            print("Stop requested, stopping!", file=sys.stderr)
            self.gfpgan = None
            self.esrgan = None

            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            gc.collect()
