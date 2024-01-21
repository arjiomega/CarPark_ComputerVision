# TODO: Remove. Only kept for reference.

import cv2
import pickle
import numpy as np
from pathlib import Path

DATA_DIR = Path(Path().absolute(), "data")

cap = cv2.VideoCapture(str(Path(DATA_DIR, "parking_vid.mp4")))

with open("CarParkPos", "rb") as f:
    posList = pickle.load(f)

width, height = (60, 30)


def checkParkingSpace(imgProcessed):
    slots_avail = len(posList)

    for index, pos in enumerate(posList):
        x, y = pos
        imgCrop = imgProcessed[y : y + height, x : x + width]

        count = cv2.countNonZero(imgCrop)

        if count < 200:
            color = (0, 255, 0)  # green
            text_color = (0, 0, 0)
        else:
            color = (0, 0, 255)  # red
            text_color = (255, 255, 255)
            slots_avail -= 1

        cv2.rectangle(img, (0 + x, y + height - 15), (x + 25, y + height), color, -1)
        cv2.putText(
            img,
            str(count),
            (x, y + height - 5),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.3,
            text_color,
            1,
        )

        cv2.rectangle(img, (x, y), (x + width, y + height), color, 2)

        sub_img = img[y : y + height, x : x + width]
        white_rect = np.zeros(sub_img.shape, dtype=np.uint8)
        white_rect[:] = color
        img[y : y + height, x : x + width] = cv2.addWeighted(
            sub_img, 0.8, white_rect, 0.2, 1.0
        )

    # car count
    cv2.rectangle(img, (0, 0), (0 + 200, 0 + 30), (0, 0, 0), -1)
    cv2.putText(
        img,
        f"Slots available: {slots_avail}/{len(posList)}",
        (0, 0 + 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        2,
    )


################################################

################################################
cv2.namedWindow("image")

cv2.createTrackbar("imgBlur_ksize", "image", 3, 31, lambda x: None)
cv2.setTrackbarMin("imgBlur_ksize", "image", 3)
cv2.createTrackbar("imgBlur_sigmaX", "image", 1, 10, lambda x: None)
cv2.setTrackbarMin("imgBlur_sigmaX", "image", 0)
cv2.createTrackbar("imgThreshold_blocksize", "image", 25, 21, lambda x: None)
cv2.setTrackbarMin("imgThreshold_blocksize", "image", 3)
cv2.createTrackbar("imgThreshold_constant", "image", 16, 25, lambda x: None)
cv2.setTrackbarMin("imgThreshold_constant", "image", -25)

# cv2.createTrackbar('imgMedian', 'image', 100, 100, lambda x: None)
# cv2.createTrackbar('kernel', 'image', 100, 100, lambda x: None)
# cv2.createTrackbar('imgDilate', 'image', 100, 100, lambda x: None)
################################################

# WRITE
fourcc = cv2.VideoWriter_fourcc(*"MPEG")
out = cv2.VideoWriter("output.avi", fourcc, 20.0, (1920, 1080))

while True:
    # first one gives current position, second gives total number of frames present in video
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        # reset frame if we reach total number of frames
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 1 is sigma x (3,3) is the dimension of corner
    # imgBlur = cv2.GaussianBlur(imgGray,(3,3),1)
    ksize = cv2.getTrackbarPos("imgBlur_ksize", "image")
    ksize = round(ksize)
    if ksize % 2 == 0:
        ksize += 1
    ksize = max(ksize, 3)
    ksize = min(ksize, 31)
    imgBlur_ksize = (ksize, ksize)
    imgBlur_sigmaX = cv2.getTrackbarPos("imgBlur_sigmaX", "image")
    imgBlur = cv2.GaussianBlur(imgGray, imgBlur_ksize, imgBlur_sigmaX)

    # convert to binary image (block size 25 and 16)
    # can add trackbar to find which value is the best
    block_size = cv2.getTrackbarPos("imgThreshold_blocksize", "image")
    constant = cv2.getTrackbarPos("imgThreshold_constant", "image")
    block_size = round(block_size)
    constant = round(constant)
    # imgThreshold = cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    #                                      cv2.THRESH_BINARY_INV,25,16)
    imgThreshold = cv2.adaptiveThreshold(
        imgBlur,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        block_size,
        constant,
    )

    # kernel size = 5
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    # kernel =
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkParkingSpace(imgDilate)

    out.write(img)
    cv2.imshow("image", img)

    # cv2.imshow("ImageBlur",imgDilate)
    c = cv2.waitKey(1)

    if c & 0xFF == ord("q"):
        break
