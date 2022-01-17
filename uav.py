from helpers import Point, euDistance


class Uav:
    def __init__(self, uav_num, coord, sim) -> None:
        self.uav_number = uav_num
        self.current_coord = coord
        self.sim = sim
        if self.uav_number % 2:
            self.current_speed = Point(0.01, 0.01)
        else:
            self.current_speed = Point(-0.01, -0.01)
        self.current_acc = Point(0.0, 0.0)
        self.wanted_speed = Point(0.01, 0.01)

    def set_speed(self, speed):
        self.wanted_speed = speed

    ## FILL THIS FUNCTION FOR YOUR ALGORITHM
    def update(self):
        aim = Point(1,1)
        if self.uav_number == 0:
            aim = Point(1,1)
        elif self.uav_number == 1:
            aim = Point(1,0)
        elif self.uav_number == 2:
            aim = Point(0,1)
        elif self.uav_number == 3:
            aim = Point(0,0)
        elif self.uav_number == 4:
            aim = Point(0.5,1.5)

        att_speed = self.calcAttractive(aim)
        rep_speed = self.calcRepulsive()

        self.current_speed = att_speed + rep_speed
        if(self.uav_number == 1):
            print("current speed of UAV%d is (%.2f, %.2f)" % (self.uav_number, self.current_speed.x, self.current_speed.y))
            print("current coord is (%.2f, %.2f)" % (self.current_coord.x, self.current_coord.y))
            print("att_speed is (%.2f, %.2f)" % (att_speed.x, att_speed.y))
            print("rep_speed is (%.2f, %.2f)" % (rep_speed.x, rep_speed.y))
        
    def calcAttractive(self, aim):
        return Point(aim.x - self.current_coord.x, aim.y - self.current_coord.y)

    def calcRepulsive(self):
        uavCoords = [uav.current_coord for uav in self.sim.uavs if uav.uav_number != self.uav_number]
        return_speed = Point(0.0,0.0)
        for uav_coord in uavCoords:
            diff = Point(self.current_coord.x - uav_coord.x, self.current_coord.y - uav_coord.y)
            if diff.length() < 0.5:
                return_speed += 1/diff

        return return_speed
