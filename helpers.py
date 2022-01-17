from math import sqrt
class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __add__(self, o):
        return Point(self.x + o.x, 
                     self.y + o.y)


def euDistance(point1, point2):
    return sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)