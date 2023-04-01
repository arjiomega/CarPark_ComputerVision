# Parking Lot Availability Counter (Computer Vision Project)

![output](https://user-images.githubusercontent.com/103622027/229244210-d41a1e83-2885-4424-ab13-2be75779c8f4.gif)

This is a computer vision project that detects location of available parking slots and total available slots available as shown in the upper left of the gif above.

## How it works
![pixels](https://i.imgur.com/VbOfkWG.png)
The availability of a slot is detected by counting the number of nonzeros in each box for each slot.

![slotpixels](https://i.imgur.com/2gjmPk1.png)
we can see here that the white pixels indicating that there is something in the slot. The number of nonzero pixels is counted for each slot and compare it to a threshold to decide if it is available or not.

## Future updates
We can see in the gif above that there are false detections and it can be improved by applying an image classification machine learning model to detect if there is a car or not in the slot. This may improve the performance of the parking lot availability counter system but it may increase the computational cost which must be also taken into consideration.

## SETUP
setup environment using miniconda
```bash
conda create --no-default-packages -n <env_name>
conda activate <env_name>
conda install python=3.9
```
install required libraries
```bash
pip install -r requirements.txt
```
prepare data
```bash
python load_data.py
```
run
```bash
python main.py
```
>press 'q' key to stop