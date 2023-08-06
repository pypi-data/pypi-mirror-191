from uuid import uuid4
from pathlib import Path
from typing import Optional

import aiofiles
import torch
from fastapi import FastAPI, UploadFile
from PIL import Image

from .opts import opts
from .detectors.detector_factory import detector_factory
import os

app = FastAPI()
model = None


def get_model():
    global model

    if model is None:
        opt = opts().init()
        os.environ['CUDA_VISIBLE_DEVICES'] = opt.gpus_str
        opt.debug = max(opt.debug, 1)
        Detector = detector_factory[opt.task]
        detector = Detector(opt)
        model = detector

    return model


@app.get("/")
async def root():
    return {"message": "Hello World"}


async def save_upload_file(upload_file: UploadFile) -> str:
    file_path = f"uploaded_images/{uuid4()}{Path(upload_file.filename).suffix}"
    async with aiofiles.open(file_path, "wb") as f:
        while content := await upload_file.read(4 * 1024):
            await f.write(content)

    return file_path


@app.post("/inference")
async def inference(image: UploadFile):
    image_path = await save_upload_file(image)
    # image = Image.open(image_path).convert("RGB")

    model = get_model()
    ret = model.run(image_path)
    return ret
