from pathlib import Path

import numpy as np
from PIL import Image
from ultralytics import YOLO

from config import config

coords_format = list[float, float, float, float]

class Yolo:
    def __init__(self, confidence:float = 0.70, _debug = False) -> None:
        self.model: YOLO = None
        self.confidence = confidence
        self._debug = _debug

    def load(self, model_path: Path = config.MODELS_DIR, model_name: str = "best.pt") -> YOLO:
        self.model = YOLO(Path(model_path, model_name))

    def inference(self, input_frame: Image.Image | np.ndarray):
        result = self.model(input_frame)

        return result[0]
