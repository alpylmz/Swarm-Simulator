from time import time
from uav import Uav
from random import uniform
from helpers import Point

import numpy as np
import time
import matplotlib.pyplot as plt


class Sim:
    def __init__(self, uav_count, time_interval = 0.01, boundaries=[Point(0,0), Point(10,10)]) -> None:
        '''
        Initialize the UAVs and set the initial positions of the UAVs.
        
        :param self: the object itself
        :param uav_count: number of UAVs
        :param time_interval: the time interval between each simulation step (optional)
        :param boundaries: a list of two Point objects, representing the boundaries of the simulation
        (optional)
        :return: None
        '''
        self.uav_count = uav_count
        self.uavs = [Uav(i,
                     Point(uniform(boundaries[0].x, boundaries[1].x), 
                           uniform(boundaries[0].y, boundaries[1].y) ), self) for i in range(uav_count)]
        
        self.time_interval = time_interval
        self.time = 0.0
        self.max_acceleration = 5.0
        self.max_jerk = 1.0
        self.max_jerk_for_time_interval = self.max_jerk / self.time_interval
        self.acc_step = 4

        self.sim_time = 0.0

        self.coords = [uav.current_coord for uav in self.uavs]

        # to run GUI event loop
        plt.ion()

        # here we are creating sub plots
        self.fig = plt.figure()
        ax = self.fig.add_subplot(111)
        x = [coord.x for coord in self.coords]
        y = [coord.y for coord in self.coords]
        self.uav_drawing, = ax.plot(x,y,label='toto',color='b',marker='o',ls='')
        self.fig.show()


        plt.xlim([-10, 10])
        plt.ylim([-10, 10])


        # setting title
        plt.title("Alp's Simulator", fontsize=20)   

        # setting x-axis label and y-axis label
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")



    def step(self):
        new_positions = []
        for uav in self.uavs:
            uav.update()

            new_acc = Point(0, 0)
            
            if uav.wanted_speed.x > uav.current_speed.x:
                new_acc.x = uav.current_acc.x + self.acc_step
            elif uav.wanted_speed.x < uav.current_speed.x:
                new_acc.x = uav.current_acc.x - self.acc_step
            
            if uav.wanted_speed.y > uav.current_speed.y:
                new_acc.y = uav.current_acc.y + self.acc_step
            elif uav.wanted_speed.y < uav.current_speed.y:
                new_acc.y = uav.current_acc.y - self.acc_step
            
            old_speed = uav.current_speed
            new_speed = uav.current_speed + new_acc * self.time_interval

            new_positions.append(uav.current_coord + (old_speed + new_speed)/2.0)
            uav.current_speed = new_speed

        for pose, uav in zip(new_positions, self.uavs):
            uav.current_coord = pose

        coords = self.getCoords()
        # updating data values
        x = [coord.x for coord in coords]
        y = [coord.y for coord in coords]
        self.uav_drawing.set_data(x,y)


        # This will run the GUI event
        # loop until all UI events
        # currently waiting have been processed
        self.fig.canvas.flush_events()

        time.sleep(self.time_interval)
        self.sim_time += self.time_interval
        plt.title("Alp's Simulator %.2f" % self.sim_time, fontsize=20)


    def getCoords(self):
        '''
        Returns a list of the current coordinates of all the UAVs in the swarm.
        
        :param self: the object that called the function
        :return: The current coordinates of each UAV.
        '''
        return [uav.current_coord for uav in self.uavs]


