import os
import json

import cv2
import numpy as np


def load_parkinglot_data(
    frame: np.ndarray = None, json_filename: str = "parkinglot_data"
):
    if f"{json_filename}.json" in os.listdir(os.curdir):
        with open(f"{json_filename}.json", "r") as f:
            parkinglot_dict = json.load(f)
    else:
        parkinglot_dict = {
            "lot_locations": [],
            "lot_dimensions": [],
            "frame_dimension": frame.shape,
            "lots_count": 0,
        }
    return parkinglot_dict


# TODO: include multiprocessing


def lot_iter_decorator(func):
    def inner(*args, **kwargs):
        parkinglot_dict: list = kwargs.get("parkinglot_dict", None)
        if parkinglot_dict is None:
            raise ValueError(
                "parkinglot_dict not provided. Add it as keyword argument. ex: parkinglot_dict=parkinglot_dict"
            )

        lot_locations = parkinglot_dict["lot_locations"]
        lot_dimensions = parkinglot_dict["lot_dimensions"]

        for lot_idx, (lot_loc, lot_dim) in enumerate(
            zip(lot_locations, lot_dimensions)
        ):
            kwargs["lot_loc"] = lot_loc
            kwargs["lot_dim"] = lot_dim
            kwargs["lot_idx"] = lot_idx

            result = func(*args, **kwargs)

        return result

    return inner


@lot_iter_decorator
def draw_lot_mask(
    lot_loc, lot_dim, frame, color=(0, 255, 0), thickness=2, *args, **kwargs
):
    lot_loc_x, lot_loc_y = lot_loc
    lot_width, lot_height = lot_dim

    cv2.rectangle(
        frame,
        (lot_loc_x, lot_loc_y),
        (lot_loc_x + lot_width, lot_loc_y + lot_height),
        color,
        thickness,
    )

    return frame
