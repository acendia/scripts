#!/usr/bin/env python3

### Author: Evangelos Kostakis
### Email: it21945@hua.gr
### Date: 2023-07-04
### Description: Script to capture the screen using mss

###  Install the following packages before running the script
# pip install opencv-python
# pip install numpy
# pip install mss
# pip install pyautogui

import cv2
import numpy as np
from mss import mss
import pyautogui
import time
import argparse


# Default values for top and left (change them to adjust the position of the bounding box)
DEFAULT_TOP = 100
DEFAULT_LEFT = 100


# Create an argument parser to parse the arguments
parser = argparse.ArgumentParser(description='Capture screen')
parser.add_argument('--top', type=int, default=DEFAULT_TOP, help='top coordinate of bounding box')
parser.add_argument('--left', type=int, default=DEFAULT_LEFT, help='left coordinate of bounding box')
parser.add_argument('--width', type=int, default=500, help='width of bounding box')
parser.add_argument('--height', type=int, default=500, help='height of bounding box')

# Parse the arguments to obtain the values
args = parser.parse_args()

# Get the values from the arguments
top = args.top
left = args.left
width = args.width
height = args.height

# Get the size of the screen
screen_size = pyautogui.size()

# Set the bounding box based on the choice (change the choice to "default" or "optimized" based on your needs)
choice = "default"

if choice == "default":
    bounding_box = {'top': top, 'left': left, 'width': screen_size.width, 'height': screen_size.height}
elif choice == "optimized":
    bounding_box = {'top': top, 'left': left, 'width': 500, 'height': 500}
elif choice == "super_optimized":
    bounding_box = {'top': top, 'left': left, 'width': 250, 'height': 250}

# Initialize the mss object to capture screenshots
sct = mss()

# Start time
start_time = time.time()
frame_count = 0

# Loop to take screenshots and display them
while True:
    # Take a screenshot of the bounding box
    sct_img = sct.grab(bounding_box)
    
    # Convert the image to a numpy array and display it
    cv2.imshow('screen', np.array(sct_img))

    # Check if the user wants to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

    # Check if the user clicked to close the window (may not work on macOS, try it on Linux)
    if cv2.getWindowProperty('screen', cv2.WND_PROP_VISIBLE) < 1:
        cv2.destroyAllWindows()
        break

    # Calculate frames per second (fps)
    elapsed_time = time.time() - start_time
    fps = frame_count / elapsed_time
    # print("fps: " + str(fps))
    print(f"fps: {fps:.2f}")
    frame_count += 1


# Calculate the total time taken
end_time = time.time()
total_time = end_time - start_time

print(f"Total time taken: {total_time:.2f} seconds")
