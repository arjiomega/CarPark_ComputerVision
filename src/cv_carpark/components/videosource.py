from typing import Callable, Any

import cv2
import numpy as np


class VideoSource:
    def __init__(self, videopath: str | int = 0) -> None:
        # Uses default camera if no path is given
        self.video_capture = cv2.VideoCapture(videopath)

    @staticmethod
    def startvid(
        func: Callable[[Any, np.ndarray], np.ndarray]
    ) -> Callable[[Any], None]:
        """
        Decorator function that starts the camera and applies a given function to each frame.

        Args:
        func (Callable[[Any, np.ndarray], np.ndarray]): The function to be applied to each frame.

        Returns:
        Callable[[Any], None]: The decorated function.
        """

        def inner(self: Any) -> None:
            """
            Inner function that reads frames from the camera, applies the given function,
            and displays the processed frame.

            Args:
            self (Any): The object instance.

            Returns:
            None
            """
            while True:
                _, frame = self.video_capture.read()
                frame = func(self, frame)
                cv2.imshow(self.window_name, frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

        return inner

    def stopvid(self: Any) -> None:
        """
        Stop the camera capture and close all windows.

        Args:
            self: The object instance.

        Returns:
            None
        """
        self.video_capture.release()
        cv2.destroyAllWindows()
