# TODO: Remove. Only kept for reference.

from pytube import YouTube
import os
import cv2
from pathlib import Path

if not os.path.exists("data"):
    os.makedirs("data")

# download the video
YouTube("https://www.youtube.com/watch?v=yojapmOkIfg").streams.filter(
    res="1080p", file_extension="mp4"
).first().download("./data", filename="parking_vid.mp4")


# take a single screenshot from the video
DATA_DIR = Path(Path().absolute(), "data")

cap = cv2.VideoCapture(str(Path(DATA_DIR, "parking_vid.mp4")))
counter = 0
while True:
    counter += 1
    ret, frame = cap.read()
    print(ret)
    if ret and counter == 50:
        cv2.imwrite(str(Path(DATA_DIR, "parking_img.png")), frame)
