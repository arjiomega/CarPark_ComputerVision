import numpy as np
from PIL import Image
from fastapi import FastAPI
from pydantic import BaseModel

from api.inference.ml import Yolo
from parking_lot.parking_lot import Cars, ParkingLot
from api.inference.by_pixel import count_lot_pixel

yolo = Yolo(_debug = True)
yolo.load()

app = FastAPI()

class InferenceRequest(BaseModel):
    image_input: list[list[list[int]]]
    coords_list: list[list[float]]


@app.post("/api/inference/by_pixel")
def inference(input_data: InferenceRequest):
    image_frame = Image.fromarray(np.array(input_data.image_input, dtype=np.uint8))
    coords_list = input_data.coords_list

    parking_lot = ParkingLot.from_list(coords_list)

    PIXEL_COUNT_FOR_OCCUPIED = 300

    for space in parking_lot.lot_iterator():
        space.is_occupied = True if count_lot_pixel(
            image_frame.crop(space.coords)
        )["non_zero_pixel_count"] > PIXEL_COUNT_FOR_OCCUPIED else False

    return_dict = {
        "parking_lot_info": parking_lot.to_dict(),
        "cars_info": None
    }

    return return_dict

@app.post("/api/inference/ml/{model_name}")
def inference_ml(model_name: str, input_data: InferenceRequest):
    image_frame = Image.fromarray(np.array(input_data.image_input, dtype=np.uint8))
    coords_list = input_data.coords_list

    parking_lot = ParkingLot.from_list(coords_list)

    if model_name == "yolo":
        result = yolo.inference(image_frame)

    cars = Cars.from_list(result.boxes.data.tolist())
        
    for car in cars.cars_iterator():
        parking_lot.park_car(car)

    return_dict = {
        "parking_lot_info": parking_lot.to_dict(),
        "cars_info": cars.to_dict()
    }

    return return_dict
