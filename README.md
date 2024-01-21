# Parking Lot Availability Counter (Computer Vision Project)

![output](https://user-images.githubusercontent.com/103622027/229244210-d41a1e83-2885-4424-ab13-2be75779c8f4.gif)

This is a computer vision project that detects location of available parking slots and total available slots available as shown in the upper left of the gif above.

## How it works
![pixels](https://i.imgur.com/VbOfkWG.png)
The availability of a slot is detected by counting the number of nonzeros in each box for each slot.

![slotpixels](https://i.imgur.com/2gjmPk1.png)
we can see here that the white pixels indicating that there is something in the slot. The number of nonzero pixels is counted for each slot and compare it to a threshold to decide if it is available or not.

## SETUP
setup environment using venv
```shell
python3.10 -m venv .env
```

load project environment (windows)
```shell
.\.env\Scripts\activate
```

install required libraries
```shell
pip install -e .
```

prepare data
```shell
python load_data.py
```

run
```shell
cv_carpark
```
>press 'q' key to stop