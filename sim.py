from time import time
from uav import Uav
from random import uniform
from helpers import Point

import numpy as np
import time
import matplotlib.pyplot as plt


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

        self.sim_time = 0.0

        self.coords = [uav.current_coord for uav in self.uavs]

        # to run GUI event loop
        plt.ion()

        # here we are creating sub plots
        self.figure, ax = plt.subplots(figsize=(10, 10))
        self.line1, = ax.plot([coord.x for coord in self.coords], [coord.y for coord in self.coords])


        # setting title
        plt.title("Alp's Simulator", fontsize=20)   

        # setting x-axis label and y-axis label
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")





    def step(self):
        for uav in self.uavs:
            uav.current_coord += uav.current_speed

        coords = self.getCoords()
        # updating data values
        self.line1.set_xdata([coord.x for coord in coords])
        self.line1.set_ydata([coord.y for coord in coords])  

        # drawing updated values
        self.figure.canvas.draw()

        # This will run the GUI event
        # loop until all UI events
        # currently waiting have been processed
        self.figure.canvas.flush_events()

        time.sleep(self.time_interval)
        self.sim_time += self.time_interval
        plt.title("Alp's Simulator " + str(self.sim_time), fontsize=20)


    def getCoords(self):
        return [uav.current_coord for uav in self.uavs]


