from helpers import Point, euDistance


class Uav:
    def __init__(self, uav_num, coord, sim) -> None:
        '''
        The constructor of the class.
        
        :param self: the object itself
        :param uav_num: the number of the UAV
        :param coord: the current coordinate of the UAV
        :param sim: the simulation object
        :return: None
        '''
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
        '''
        Set the speed of the UAV.
        
        :param self: This is a reference to the instance of the class
        :param speed: The speed you want to go at
        :return: None
        '''
        self.wanted_speed = speed

    ## FILL THIS FUNCTION FOR YOUR ALGORITHM
    def update(self):
        '''
        The function calculates the attractive and repulsive force for each UAV and sums them up to get
        the current speed of each UAV.
        
        :param self: the object itself
        :return: None
        '''
        aim = Point(1,1)
        if self.uav_number == 0:
            aim = Point(2,2)
        elif self.uav_number == 1:
            aim = Point(2,0)
        elif self.uav_number == 2:
            aim = Point(0,2)
        elif self.uav_number == 3:
            aim = Point(0,0)
        elif self.uav_number == 4:
            aim = Point(1,1)

        att_speed = self.calcAttractive(aim)
        rep_speed = self.calcRepulsive()

        self.wanted_speed = att_speed * 0.1 + rep_speed * 0.4
        if(self.uav_number == 1):
            print("current speed of UAV%d is (%.2f, %.2f)" % (self.uav_number, self.current_speed.x, self.current_speed.y))
            print("current coord is (%.2f, %.2f)" % (self.current_coord.x, self.current_coord.y))
            print("att_speed is (%.2f, %.2f)" % (att_speed.x, att_speed.y))
            print("rep_speed is (%.2f, %.2f)" % (rep_speed.x, rep_speed.y))
        
    def calcAttractive(self, aim):
        '''
        Calculate the attractive force of the aim point to the current point.
        
        :param self: This is a reference to the object that is calling the method
        :param aim: the point we want to get to
        :return: The attractive force is a vector that points from the current position to the target
        position.
        '''
        return Point(aim.x - self.current_coord.x, aim.y - self.current_coord.y)

    def calcRepulsive(self):
        '''
        Calculate the repulsive force for a UAV.
        
        :param self: the object that called the function
        :return: The speed of the UAV.
        '''
        uavCoords = [uav.current_coord for uav in self.sim.uavs if uav.uav_number != self.uav_number]
        return_speed = Point(0.0,0.0)
        for uav_coord in uavCoords:
            diff = Point(self.current_coord.x - uav_coord.x, self.current_coord.y - uav_coord.y)
            if diff.length() < 0.5:
                return_speed += 1/diff

        return return_speed
