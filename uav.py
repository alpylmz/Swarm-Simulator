from helpers import Point


class Uav:
    def __init__(self, uav_num, coord) -> None:
        self.uav_number = uav_num
        self.current_coord = coord
        if self.uav_number % 2:
            self.current_speed = Point(0.01, 0.01)
        else:
            self.current_speed = Point(-0.01, -0.01)
        self.current_acc = Point(0.0, 0.0)
        self.wanted_speed = Point(0.01, 0.01)

    def set_speed(self, speed):
        self.wanted_speed = speed

    def update(self):
        pass
        ## FILL THIS FUNCTION FOR YOUR ALGORITHM

    
