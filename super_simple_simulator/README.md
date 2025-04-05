# Super Simple Robot Simulator

This is a super simple version of the robot simulator built using Pygame. By understanding this script, you grasp the main idea behind simulating a differential-drive robot by controlling its linear and angular velocities.

You can change this script to implement your own algortithms to control the robot.

## Requirements

- Python 3.10 or higher
- Pygame
- NumPy

## Installation

In case you need to install stuff:

1. Install Python 3.10 (or higher) from [python.org](https://www.python.org/).
2. Install Pygame using pip:
    ```
    pip install pygame
    ```
3. Install NumPy using pip:
    ```
    pip install numpy
    ```


## Usage

1. Clone the repository or download the source code.
2. Run the 

simple_robot_simulator.py

 file:
    ```
    python simple_robot_simulator.py
    ```

## Controls

When the simulator starts, the robot will be at the center of the screen. 

With the mouse, you can click where you want to place the robot at any point during the simulation. You can further control it with the keyboard.

While the simulator is running, you can press the following keys to change its behavior:

- **Up/Down Arrow Keys**: Move the robot forward/backwards
- **Left/Right Arrow Keys**: Rotate the robot counterclockwise/clockwise
- **C**: **Center** the robot on the screen
- **9**: rotate the robot by **+90** degrees
- **P**: toggle **Printing** of robot position on the screen
- **S**: toggle **Showing path** on the screen
- **R**: **Reset** the position of the robot 
- **T**: draw a **Triangle** to indicate the orientation of the robot
- **Q**: **Quit** the program

## Code Overview

The main components of the code are:

- **Pygame Setup**: Initializes Pygame, sets up the screen, and loads assets.
- **Robot Movement Functions**: Functions to apply linear and angular movement to the robot.
- **Main Loop**: Handles events, updates the robot's position and orientation, and renders the screen.

Feel free to modify and extend the simulator as needed. Enjoy controlling your robot!

## License

This project is licensed under the MIT License. See the LICENSE file in the main folder for details.
