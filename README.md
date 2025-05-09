# Simple Robot Simulator

This is a simple robot simulator built using Pygame. For now, the working version simulates only a **differential-drive robot**. It can use **Dijkstra's algorithm** to define waypoints for the robot to follow, implements a **path-following** algorithm using **PID**, and allows you to control the robot using the keyboard and mouse. It also implements (very) crude reaction to obstacle collision. 

With this simulator, the idea is that you can write your own algortithms like controllers, planning, obstacle avoidance etc. 

The code is divided in different files, each one implementing a specific function of the simulator (robot and its functions, path-planning, controller etc.). If you are a beginner, you might be interested in the **super simple** version of the simulator, which is available in the corresponding folder.

## Running the Simple Robot Simulator

The animation below shows the simulator running. You can see a robot in a grid world with some obstacles in blue. The buttons on the right allow you to access functions of the simulator. For instance, you can define the start and goal positions, and the planning algorithm will generate a sequence of waypoints for the robot to follow. The path it followed since the simulation started can also be shown (in blue). A PID controller is used to control the orientation of the robot towards the next waypoint, which is also shown in blue. The robot can also be controlled manually (via the arrow keys on the keyboard), and can be manually placed in any position of the map.

![Simple Robot Simulator](SimRobSim_path-planning-following.gif)

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

open_world_simulator.py

 file:
    ```
    python open_world_simulator.py
    ```

## Controls

When the simulator starts, the robot will be at some starting position, defined by the variable 'robot_start_coords'. If you click the "Place robot" button, you can mouse-click anywhere in the map to place the robot at any point during the simulation. You can further control it with the keyboard.

Besides the buttons, some functions can also be activated via the keyboard: 

- **Up/Down Arrow Keys**: Move the robot forward/backwards
- **Left/Right Arrow Keys**: Rotate the robot counterclockwise/clockwise
- **C**: **Center** the robot on the screen
- **9**: rotate the robot by **+90** degrees
- **P**: toggle **Printing** of robot position on the screen
- **S**: toggle **Showing path** on the screen
- **R**: **Reset** the position of the robot path and achieved waypoints
- **T**: toggle a **Triangle** to indicate the orientation of the robot
- **W**: toggle displaying the **Waypoints** on the screen
- **F**: toggle the controller to **Follow** the path defined by the waypoints
- **=**: increase the robot speed
- **-**: decrease the robot speed
- **Q**: **Quit** the program

## Code Overview

The main components of the code are:

- **Pygame Setup**: Initializes Pygame, sets up the screen, and loads assets.
- **Robot Movement Functions**: Functions to apply linear and angular movement to the robot.
- **Path Follower**: Class that generates angular speed to move the robot across a list of waypoints. 
- **Path Planner**: Class that implements Dijkstra's algorithm to plan a path from start to goal avoiding obstacles.
- **Main Loop**: Handles events, updates the robot's position and orientation, and renders the screen.

## To do

There are tons of things to do! 

- Fix the reaction to obstacle collision: at the moment, collision is only detected by checking the position of the center of the robot. Besides, the if the robot is moving backwards, it will cross the obstacle.
- Organize the entire code in classes (on-going) to separate the code into independent parts. The idea (dream) is:

* Robot class
    - Add a dynamic model to more accurately simulate the robot behavior
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

* Perception class
    - State estimation 
    - Kalman filters
    - Particle filters
    - SLAM

* Obstacles class (implemented)
    - Dynamics obstacles
        - Proxemics
        - Potential fields
    - Static obstacles (implemented)

* World class
    - World parameters
    - Automate obstacle creation with the mouse
    - Correlate world map with grip_map in Dijkstra

* Planning Algorithms class
    - Dijkstra (implemented)
    - A*
    - D*

* Controller class
    - PID to control orientation (implemented in the path follower)
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