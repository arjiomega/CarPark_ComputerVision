import numpy as np
from PIL import Image
from fastapi import FastAPI
from pydantic import BaseModel

from api.inference.by_pixel import predict_by_pixel_count

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


class InferenceRequest(BaseModel):
    image_input: list[list[list[int]]]
    coords_list: list[list[float]]


@app.post("/api/inference/by_pixel")
def inference(input_data: InferenceRequest):

    image_frame = Image.fromarray(np.array(input_data.image_input, dtype=np.uint8))

    labels = predict_by_pixel_count(image_frame, input_data.coords_list)

    output = {
        str(idx): {
            "coords": coords,
            "label": label,
        }
        for idx, (coords, label) in enumerate(zip(input_data.coords_list, labels))
    }

    return output


@app.post("/api/inference/ml/{model_name}")
def inference(model_name: str, input_data: InferenceRequest):

    image_frame = Image.fromarray(np.array(input_data.image_input, dtype=np.uint8))

    labels = predict_by_pixel_count(image_frame, input_data.coords_list)

    output = {
        str(idx): {
            "coords": coords,
            "label": label,
        }
        for idx, (coords, label) in enumerate(zip(input_data.coords_list, labels))
    }

    return output
