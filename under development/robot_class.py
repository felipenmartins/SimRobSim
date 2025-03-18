from abc import ABC, abstractmethod
from controller_class import Controller
from planner_class import Planner
import math

# class Robot(ABC):
class Robot:
    '''
    A class to represent a robot.
    '''
    MAX_LIN_SPEED = 100  # pixels per second
    MAX_ANG_SPEED = 1.58   # radians per second
    ROBOT_SIZE = 100    # not in use

    def __init__(self, 
                 dt, # time step from the simulation
                 name='Lucy', 
                 company='Robotis', 
                 model='Turtlebot-burger',
                 robot_img="roomba-top-view-removebg.png",
                 ):
        self.dt=dt
        self.name=name
        self.company=company
        self.model=model
        self.pose = [0,0,0]
        self.robot_img = robot_img
        self.lin_speed = 0
        self.ang_speed = 0
        self.controller=Controller(self)
        self.planner=Planner(self)

    def move(self, **kwargs):
        '''
        Move the robot in the direction it is facing, then rotate it.
        Output its new pose.
        '''
        # lin_speed=self.lin_speed, ang_speed=self.ang_speed, robot_pose=self.pose, dt=self.dt
        lin_speed= kwargs.get('lin_speed', self.lin_speed)
        ang_speed= kwargs.get('ang_speed', self.ang_speed)
        robot_pose= kwargs.get('robot_pose', self.pose)
        dt= kwargs.get('dt', self.dt)
        
        # Limit the linear and angular speeds to the maximum values
        lin_speed = min(lin_speed, self.MAX_LIN_SPEED)
        lin_speed = max(lin_speed, -self.MAX_LIN_SPEED)
        ang_speed = min(ang_speed, self.MAX_ANG_SPEED)
        ang_speed = max(ang_speed, -self.MAX_ANG_SPEED)

        # Update the robot's pose
        robot_pose[0] += lin_speed * math.cos(robot_pose[2]) * dt
        robot_pose[1] -= lin_speed * math.sin(robot_pose[2]) * dt
        robot_pose[2] += ang_speed * dt

        # Limit the robot orientation to [-pi, pi]
        robot_pose[2] = (robot_pose[2] + math.pi) % (2 * math.pi) - math.pi

        # Return the new pose
        return robot_pose

    def set_pose(self, new_pose):
        self.pose=new_pose

    def get_pose(self):
        return self.pose
    

class Diff_Drive(Robot):
    # ???
    pass