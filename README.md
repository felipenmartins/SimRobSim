# Simple Robot Simulator

This is a simple robot simulator built using Pygame. For now, the working version of the simulator allows you to control a differential-drive robot on the screen using the keyboard and mouse. The idea is that you can write your own controller to generate commands to the robot. 

The screenshot below shows the simulator running. You can see a robot and the path it followed since the simulation started.

![Simple Robot Simulator screenshot](SimRobSim.png)

The folder 'under development' contains the version being developed at the moment. It is recommended that you use the files from the main folder.

## Requirements

- Python 3.10 or higher
- Pygame

## Installation

1. Install Python 3.10 (or higher) from [python.org](https://www.python.org/).
2. Install Pygame using pip:
    ```
    pip install pygame
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

- **Up/Down Arrow Keys**: Move the robot forward/backwards
- **Left/Right Arrow Keys**: Rotate the robot counterclockwise/clockwise
- **C**: Center the robot on the screen
- **9**: Rotate the robot by +90 degrees
- **P**: Toggle printing of robot position on the screen
- **S**: Toggle showing the robot path on the screen
- **R**: Clear the memory of the robot path
- **T**: Draw a triangle to indicate the orientation of the robot

## Code Overview

The main components of the code are:

- **Pygame Setup**: Initializes Pygame, sets up the screen, and loads assets.
- **Robot Movement Functions**: Functions to apply linear and angular movement to the robot.
- **Main Loop**: Handles events, updates the robot's position and orientation, and renders the screen.

## To do

There is a ton of things to do! For now, creating classes to separate the code into independent parts is the priority. The idea is:

* Robot class
    - Have different robot names
	- Combine a profile type with specific sensors and parameters (speed, sensor range etc.)
    - Different profiles for robots 
        - Differential-drive (implemented)
        - Car-like
        - Omnidirectional

* Create a Sensors class
    - IMU
    - LiDAR
    - Wheel encoders
    - IR distance sensors
    - IR for line following
* Sensor Noise class 

* Obstacles class
    - Dynamics obstacles
        - Proxemics
        - Potential fields
    - Static obstacles

* Grid class
    - World parameters

* Planning Algorithms class
    - Dijkstra
    - A*
    - D*

* Perception class
    - State estimation 
    - Kalman filters
    - Particle filters
    - SLAM

* Controller class
    - PID to control orientation
    - Trajectory tracking to control speed and orientation
    - Other simple behaviors

* State machine to select controllers or simple behaviors to:
    - Go-to-goal
    - Line following
    - Path following
	- Obstacle avoidince
    - Maze solving


## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

- Praveen K. for teaching me a lot of Python and helping me create this simulator.

---

Feel free to modify and extend the simulator as needed. Enjoy controlling your robot!