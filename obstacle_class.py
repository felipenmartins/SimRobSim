import pygame
import numpy as np

class Obstacle:
    def __init__(self, origin,color):
        self.x = origin[0]
        self.y = origin[1]
        self.color = color
        

class CircularObstacle(Obstacle):
    def __init__(self, origin, radius,color):
        super().__init__(origin,color)
        self.radius = radius

class RectangularGridObstacle():
    def __init__(self):
        self.obstacles = np.array([
            [1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]) # Transpose the grid to match the orientation of the world
        

class RectangularObstacle(Obstacle):
    def __init__(self, origin, color, width, height):
        super().__init__(origin,color)
        self.width = width
        self.height = height
        self.obs=  pygame.Rect(self.x,self.y,self.width,self.height)

class PolygonObstacle(Obstacle):
    def __init__(self, origin,color, vertices):
        super().__init__(origin,color)
        self.vertices=vertices

    
      