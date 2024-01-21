# TODO: Remove. Only kept for reference.

import cv2
import pickle
import numpy as np
from pathlib import Path

DATA_DIR = Path(Path().absolute(), "data")

img = cv2.imread(str(Path(DATA_DIR, "parking_img.png")))


width, height = (60, 30)

try:
    with open("CarParkPos", "rb") as f:
        posList = pickle.load(f)
except:
    posList = []


def mouseclick(events, x, y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((x, y))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(posList):
            x1, y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)

    with open("CarParkPos", "wb") as f:
        pickle.dump(posList, f)

    return 0


def checkParkingSpace():
    for pos in posList:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (255, 0, 255), 2)


cv2.namedWindow("image", cv2.WINDOW_GUI_NORMAL)
while True:
    img = cv2.imread(str(Path(DATA_DIR, "parking_img.png")))
    # cv2.rectangle(img,(100,100),(200,150),(255,0,255),2)

    checkParkingSpace()

    cv2.imshow("image", img)
    cv2.setMouseCallback("image", mouseclick)
    cv2.waitKey(1)
