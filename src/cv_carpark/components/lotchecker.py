import cv2
import numpy as np


def count_lot_pixel(lot_frame):
    lot_frame = cv2.cvtColor(lot_frame, cv2.COLOR_BGR2GRAY)

    ksize = 3
    imgBlur_ksize = (ksize, ksize)
    imgBlur_sigmaX = 1
    lot_frame = cv2.GaussianBlur(lot_frame, imgBlur_ksize, imgBlur_sigmaX)

    block_size = 25
    constant = 16
    lot_frame = cv2.adaptiveThreshold(
        lot_frame,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        block_size,
        constant,
    )

    kernel_size = 5
    lot_frame = cv2.medianBlur(lot_frame, kernel_size)

    kernel = np.ones((3, 3), np.uint8)
    lot_frame = cv2.dilate(lot_frame, kernel, iterations=1)

    return cv2.countNonZero(lot_frame)
