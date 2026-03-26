# Motion Detection with Buzzer using Raspberry Pi

## Description
This project implements a real-time motion detection system using OpenCV on Raspberry Pi. When motion is detected, a buzzer is triggered as an alert.

## Objective
To build a simple security system using computer vision and embedded hardware.

## Hardware Required
* Raspberry Pi 4
* USB Camera / Pi Camera
* Buzzer
* Breadboard & Jumper wires

## Software Used
* Python 3
* OpenCV
* RPi.GPIO

## Installation
```bash
sudo apt update
sudo apt install python3-pip
pip3 install opencv-python RPi.GPIO
```

## Run the Project
```bash
python3 src/motion_detection.py
```

## GPIO Connection
* Buzzer → GPIO 18
* GND → Ground

## Working
* Captures continuous video frames
* Computes difference between consecutive frames
* Applies thresholding and contour detection
* If motion is detected:

  * Bounding box is drawn
  * Buzzer is activated

## Future Improvements
* Add camera recording on motion
* Send alerts to mobile
* Human detection using AI models
* Cloud integration


