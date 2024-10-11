from pathlib import Path

import numpy as np
from PIL import Image
from ultralytics import YOLO


from config import config

coords_format = list[float, float, float, float]

def calculate_iou(box_A: coords_format, box_B: coords_format):
    # https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTTKKX7PzlRgQWRUs5edCqHno6k6Aul9x-EYu1qn0TvZbAaiXU9gfVyW2bItCTG8H92Ng&usqp=CAU
    x_intersection_A, y_intersection_A = max(box_A[0], box_B[0]), max(box_A[1], box_B[1])
    x_intersection_B, y_intersection_B = max(box_A[2], box_B[2]), max(box_A[3], box_B[3])

    intersection_area = max(0, x_intersection_B - x_intersection_A) * max(0, y_intersection_B - y_intersection_A)

    # Calculate the area of both boxes
    boxAArea = (box_A[2] - box_A[0]) * (box_A[3] - box_A[1])
    boxBArea = (box_B[2] - box_B[0]) * (box_B[3] - box_B[1])

    # Calculate the IoU
    iou = intersection_area / float(boxAArea + boxBArea - intersection_area)

    return iou

class Yolo:
    def __init__(self) -> None:
        self.model: YOLO = None

    def load(self, model_path: Path = config.MODELS_DIR, model_name: str = "best.pt") -> YOLO:
        self.model = YOLO(Path(model_path, model_name))

    def inference(self, input_frame: Image.Image | np.ndarray, coords: list[coords_format]) -> list[list[float]]:
        result = self.model(input_frame)

        for frame in result:
            for box in frame.boxes.data.tolist():
                x1, y1, x2, y2, confidence, class_id = box

                iou = calculate_iou()

    def get_bounding_boxes():
        pass