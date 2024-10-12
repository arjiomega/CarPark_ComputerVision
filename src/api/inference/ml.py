from pathlib import Path

import numpy as np
from PIL import Image
from ultralytics import YOLO

from utils.img_preprocess import get_centroid, is_inside_boundary
from config import config

coords_format = list[float, float, float, float]

model = 

class Yolo:
    def __init__(self, confidence:float = 0.70) -> None:
        self.model: YOLO = None
        self.confidence = confidence

    def load(self, model_path: Path = config.MODELS_DIR, model_name: str = "best.pt") -> YOLO:
        self.model = YOLO(Path(model_path, model_name))

    def inference(self, input_frame: Image.Image | np.ndarray, coords: list[coords_format]) -> list[list[float]]:
        result = self.model(input_frame)

        output_list = []

        # loop coords of parking lot instead

        for frame in result: # single frame == single batch
            curr_frame_labels = []
            for box in frame.boxes.data.tolist():
                x1, y1, x2, y2, confidence, class_id = box

                # skip if below confidence
                if confidence < self.confidence:
                    continue

                car_centroid_x, car_centroid_y = get_centroid((x1, y1, x2, y2))
                label = is_inside_boundary(coords, (car_centroid_x, car_centroid_y))

                curr_frame_labels.append(label)

            output_list.append(curr_frame_labels)
                
        return output_list


    def get_bounding_boxes():
        pass