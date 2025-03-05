from abc import ABC
from controller_class import Controller
from planner_class import Planner

class Robot(ABC):
    LIN_SPEED = 80  # pixels per second
    ANG_SPEED = 1   # radians per second
    ROBOT_SIZE = 100    # not in use

    def __init__(self, 
                 name='Lucy', 
                 company='Robotis', 
                 model='Turtlebot-burger',
                 robot_img="roomba-top-view-removebg.png",
                 ):
        self.name=name
        self.company=company
        self.model=model
        self.pose = (0,0,0)
        self.robot_img = robot_img
        self.controller=Controller(self)
        self.planner=Planner(self)

    def move(self, direction):
        pass

    def set_pose(self,new_pose):
        self.pose=new_pose

    def get_pose(self):
        return self.pose
    
