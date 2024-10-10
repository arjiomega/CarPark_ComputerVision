import json
from fastapi import FastAPI, Depends

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

import numpy as np
from api.utils import predict_by_pixel_count

from pydantic import BaseModel
from typing import List
from PIL import Image

class InferenceRequest(BaseModel):
    image_input: List[List[List[int]]] 
    coords_list: List[List[float]]
@app.post("/api/inference/{inference_type}/{model_name}")
def inference(test_a: str, model_name: str, input_data: InferenceRequest):

    image_frame = Image.fromarray(
        np.array(input_data.image_input, dtype=np.uint8)
    )

    labels = predict_by_pixel_count(image_frame, input_data.coords_list)

    output = {
        str(idx): {
            "coords": coords,
            "label": label,
        }
        for idx, (coords, label) in enumerate(zip(input_data.coords_list, labels))
    }

    return output