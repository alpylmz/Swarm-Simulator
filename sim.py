from time import time
from uav import Uav
from random import uniform
from helpers import Point

class Sim:
    def __init__(self, uav_count, time_interval = 0.01, boundaries=[Point(0,0), Point(10,10)]) -> None:
        self.uav_count = uav_count
        self.uavs = [Uav(i,
                     Point(uniform(boundaries[0].x, boundaries[1].x), 
                           uniform(boundaries[0].y, boundaries[1].y) )) for i in range(uav_count)]
        
        self.time_interval = time_interval
        self.time = 0.0
        self.max_acceleration = 5.0
        self.max_jerk = 1.0
        self.max_jerk_for_time_interval = self.max_jerk / self.time_interval


    def step(self):
        for uav in self.uavs:
            uav.current_coord += uav.current_speed

        return [uav.current_coord for uav in self.uavs]

    def getCoords(self):
        return [uav.current_coord for uav in self.uavs]


