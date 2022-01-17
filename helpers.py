from math import sqrt
class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __add__(self, o):
        return Point(self.x + o.x, 
                     self.y + o.y)

    def __mul__(self, o):
        return Point(self.x * o,
                     self.y * o)

    def __rmul__(self, o):
        return Point(self.x * o,
                     self.y * o)

    def __truediv__(self, o):
        return Point(self.x / o,
                     self.y / o)

    def __rtruediv__(self, o):
        return Point(o / self.x,
                     o / self.y)

    def length(self):
        return sqrt(self.x**2 + self.y**2)

def euDistance(point1, point2):
    return sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

