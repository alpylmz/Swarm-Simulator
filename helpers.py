class Point:
    def __init__(self, x, y) -> None:
        self.x = x
        self.y = y

    def __add__(self, o):
        return Point(self.x + o.x, 
                     self.y + o.y)