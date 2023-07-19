# Screen Capture Script

## Description

This script captures the screen using the `mss` library in Python. It allows you to specify the position and size of the bounding box to capture. The captured screen is displayed in a window, and the frames per second (fps) is calculated and printed on the console. You can quit the script by pressing the 'q' key or closing the window.

## Features

- Capture the screen using a specified bounding box
- Display the captured screen in a window
- Calculate and print frames per second (fps)
- Quit the script by pressing the 'q' key or closing the window

## Installation

Before running the script, make sure to install the following packages:

- opencv-python
- numpy
- mss
- pyautogui

You can install the dependencies using pip:

```shell
pip install -r requirements.txt
```

## Usage

Run the script using the following command:
```shell
python script_capture_screen.py [--top TOP] [--left LEFT] [--width WIDTH] [--height HEIGHT] [--choice CHOICE]
```

Optional arguments:
- --top: The top coordinate of the bounding box (default: 100).
- --left: The left coordinate of the bounding box (default: 100).
- --width: The width of the bounding box (default: 500).
- --height: The height of the bounding box (default: 500).
- --choice: The choice for bounding box size (default: "super_optimized").

You can adjust the position and size of the bounding box according to your needs. The choice parameter allows you to select different sizes for the bounding box.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or feature requests, please open an issue or submit a pull request.

## License

This script is released under the MIT License.




