from pathlib import Path

import cv2
import numpy as np

from cv_carpark.components import videosource, utils, lotchecker
from cv_carpark import config

# TODO: Add available lots
class CarParkAvailability(videosource.VideoSource):
    def __init__(self, videopath: str | int = 0) -> None:
        """
        Initialize the CarParkAvailability object.

        Args:
        - videopath: The path to the video source (default is the webcam).
        """
        super().__init__(videopath=videopath)
        self.window_name = "Car Park Availability Counter"
        self.parkinglot_dict = utils.load_parkinglot_data()
        self._set_window_properties()

    @videosource.VideoSource.startvid
    def run(self, frame:np.ndarray):
        """
        Process each frame of the video to determine the availability of parking lots.

        Args:
        - frame: The input frame to be processed.

        Returns:
        - np.ndarray: The processed frame with parking lot availability highlighted.
        """
        frame = self._preprocess_lot(frame=frame, parkinglot_dict=self.parkinglot_dict)
        return frame

    @utils.lot_iter_decorator
    def _preprocess_lot(
        self, 
        frame: np.ndarray,
        lot_idx: int, 
        lot_loc:tuple[int,int], 
        lot_dim:tuple[int,int], 
        *args, 
        **kwargs
    ) -> np.ndarray:
        """
        Preprocess a specific parking lot within the frame.

        Args:
        - frame: The input frame.
        - lot_idx: The index of the parking lot.
        - lot_loc: The location of the parking lot.
        - lot_dim: The dimensions of the parking lot.

        Returns:
        - np.ndarray: The frame with the processed parking lot.
        """
        
        lot_loc_x, lot_loc_y = lot_loc
        lot_width, lot_height = lot_dim

        framecrop = frame[
            lot_loc_y : lot_loc_y + lot_height, lot_loc_x : lot_loc_x + lot_width
        ]

        count = lotchecker.count_lot_pixel(framecrop)
        lot_available = count < 300

        green = (0, 255, 0)
        red = (0, 0, 255)
        white = (255, 255, 255)
        black = (0, 0, 0)
        lot_color = green if lot_available else red
        text_color = black if lot_available else white

        # Overlay a color on each lot based on availability
        status_box = np.zeros(framecrop.shape, dtype=np.uint8)
        status_box[:] = lot_color
        frame[
            lot_loc_y : lot_loc_y + lot_height, lot_loc_x : lot_loc_x + lot_width
        ] = cv2.addWeighted(framecrop, 0.8, status_box, 0.2, 1.0)

        # Text inside each lot
        cv2.putText(
            frame,
            "",
            (lot_loc_x, lot_loc_y + lot_height - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            text_color,
            1,
        )

        return frame

    def _set_window_properties(self):
        """
        Set the properties of the display window for the processed video.
        """
        cv2.namedWindow(self.window_name, cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty(
            self.window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_NORMAL
        )


def main():
    videopath = str(Path(config.DATA_DIR, "parking_lot.mp4"))

    carpark = CarParkAvailability(videopath)
    carpark.run()
    carpark.stopvid()


if __name__ == "__main__":
    # TODO: generate mask directly while predicting parking space availability
    # TODO: instead of downloading video, load video directly using pytube

    main()
