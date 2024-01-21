import json
from pathlib import Path

import cv2

from cv_carpark import config
from cv_carpark.components import utils


class Keys:
    STOP_KEY = ord("q")
    NEW_WINDOW_KEY = ord("w")


class MaskGenerator(Keys):
    # Draw a lot mask then adjust each lot size
    def __init__(
        self, parkinglot_imgpath, json_filename: str = "parkinglot_data"
    ) -> None:
        self.parkinglot_imgpath = parkinglot_imgpath
        self.parkinglot_dict = utils.load_parkinglot_data(
            frame=cv2.imread(self.parkinglot_imgpath)
        )
        self.window_name = "mask generator"
        self.json_filename = json_filename
        self.lot_dimension = (60, 30)
        self.settings()

    def settings(self):
        cv2.namedWindow(self.window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(
            self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL
        )

    def add_parkinglot(self, lot_location, lot_dimension):
        self.parkinglot_dict["lot_locations"].append(lot_location)
        self.parkinglot_dict["lot_dimensions"].append(lot_dimension)
        self.parkinglot_dict["lots_count"] = len(self.parkinglot_dict["lot_locations"])

    @utils.lot_iter_decorator
    def remove_parkinglot(
        self, lot_loc, lot_dim, mousepointer_x, mousepointer_y, *args, **kwargs
    ):
        lot_loc_x, lot_loc_y = lot_loc
        lot_width, lot_height = lot_dim
        boundary_rule_x = lot_loc_x < mousepointer_x < lot_loc_x + lot_width
        boundary_rule_y = lot_loc_y < mousepointer_y < lot_loc_y + lot_height

        if boundary_rule_x and boundary_rule_y:
            self.parkinglot_dict["lot_locations"].remove(lot_loc)
            self.parkinglot_dict["lot_dimensions"].remove(lot_dim)
            self.parkinglot_dict["lots_count"] = len(
                self.parkinglot_dict["lot_locations"]
            )

    def mousecallback(self, events, x, y, *args, **kwargs):
        match events:
            case cv2.EVENT_LBUTTONDOWN:
                self.add_parkinglot((x, y), self.lot_dimension)
            case cv2.EVENT_RBUTTONDOWN:
                self.remove_parkinglot(
                    mousepointer_x=x,
                    mousepointer_y=y,
                    parkinglot_dict=self.parkinglot_dict,
                )
            case _:
                pass

    def run(self):
        while True:
            frame = cv2.imread(self.parkinglot_imgpath)
            if self.parkinglot_dict["lots_count"] > 0:
                frame = utils.draw_lot_mask(
                    frame=frame, parkinglot_dict=self.parkinglot_dict
                )
            # Interact with cv2 frame output (add parking lots)
            cv2.setMouseCallback(self.window_name, self.mousecallback)

            cv2.imshow(self.window_name, frame)

            if cv2.getWindowProperty("lot_settings", cv2.WND_PROP_VISIBLE) == 1:
                # width, height
                width = cv2.getTrackbarPos("lot_width", "lot_settings")
                height = cv2.getTrackbarPos("lot_height", "lot_settings")
                self.lot_dimension = (width, height)

            # run key commands
            run_status = self.keys()
            if run_status == "stop":
                break

    def save_masks_local(self):
        pass

    def keys(self):
        key = cv2.waitKey(1) & 0xFF

        match key:
            case Keys.STOP_KEY:
                with open(f"{self.json_filename}.json", "w") as f:
                    json.dump(self.parkinglot_dict, f, indent=4)
                return "stop"
            case Keys.NEW_WINDOW_KEY:
                cv2.namedWindow("lot_settings")
                cv2.resizeWindow("lot_settings", width=400, height=100)
                cv2.createTrackbar("lot_width", "lot_settings", 10, 300, lambda x: None)
                cv2.setTrackbarMin("lot_width", "lot_settings", 10)
                cv2.createTrackbar(
                    "lot_height", "lot_settings", 10, 300, lambda x: None
                )
                cv2.setTrackbarMin("lot_height", "lot_settings", 10)

        return None


def main():
    parkinglot_imgpath = str(Path(config.DATA_DIR, "parking_img.png"))

    mask_generator = MaskGenerator(parkinglot_imgpath)
    mask_generator.run()


if __name__ == "__main__":
    main()
