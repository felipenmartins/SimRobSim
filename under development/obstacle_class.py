class Obstacle:
    def __init__(self, origin,color):
        self.x = origin[0]
        self.y = origin[1]
        self.color = color

class CircularObstacle(Obstacle):
    def __init__(self, origin, radius,color):
        super().__init__(origin,color)
        self.radius = radius



class RectangularObstacle(Obstacle):
    def __init__(self, origin, color, width, height):
        super().__init__(origin,color)
        self.width = width
        self.height = height

class PolygonObstacle(Obstacle):
    def __init__(self, origin,color, vertices):
        super().__init__(origin,color)
        self.vertices=vertices

    
      