from re import M
from time import time
from agent import Agent
from random import uniform
from helpers import Point, euDistance

import numpy as np
import time
import matplotlib.pyplot as plt
import sys
import signal
import json
import argparse

def _on_close(event):
    plt.close('all')
    sys.exit(0)


class Sim:
    def __init__(self, agent_count, time_interval = 0.01, boundaries=[Point(0,0), Point(10,10)]) -> None:
        '''
        Initialize the agents and set the initial positions of the agents.
        
        :param self: the object itself
        :param agent_count: number of agents
        :param time_interval: the time interval between each simulation step (optional)
        :param boundaries: a list of two Point objects, representing the boundaries of the simulation
        (optional)
        :return: None
        '''
        # a signal handler to catch CTRL+C and Z
        signal.signal(signal.SIGINT, self.close_signal_handler)
        signal.signal(signal.SIGTSTP, self.close_signal_handler)

        self.agent_count = agent_count
        self.agents = [Agent(i,
                     Point(uniform(boundaries[0].x, boundaries[1].x), 
                           uniform(boundaries[0].y, boundaries[1].y) ), self) for i in range(agent_count)]
        
        self.time_interval = time_interval
        self.time = 0.0
        self.max_acceleration = 3.0
        self.max_jerk = 1.0
        self.max_jerk_for_time_interval = self.max_jerk / self.time_interval
        self.acc_step = 1
        self.collision_warn_dist = 0.3
        self.collision_err_dist = 0.1

        self.sim_time = 0.0

        self.target = Point(1, 1)
        self.target_update_state = 0

        self.coords = [agent.current_coord for agent in self.agents]

        # to run GUI event loop
        plt.ion()

        # here we are creating sub plots
        self.fig = plt.figure()
        ax = self.fig.add_subplot(111)
        x = [coord.x for coord in self.coords]
        y = [coord.y for coord in self.coords]
        self.agent_drawing, = ax.plot(x,y,label='toto',color='b',marker='o',ls='')
        self.target_drawing, = ax.plot(self.target.x, self.target.y, color='r', marker='o')
        self.fig.show()

        self.fig.canvas.mpl_connect('close_event', _on_close)


        plt.xlim([-10, 10])
        plt.ylim([-10, 10])


        # setting title
        plt.title("Alp's Simulator", fontsize=20)   

        # setting x-axis label and y-axis label
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")



    def step(self):
        '''
        The function updates the positions of the agents and checks for collisions.
        
        :return: None
        '''
        print("Target speed is " + str(self.agents[0].wanted_speed))
        print("Current speed is " + str(self.agents[0].current_speed))
        self.updateTarget()
        new_positions = []
        for agent in self.agents:
            agent.update()

            new_acc = Point(0, 0)
            
            if agent.wanted_speed.x > agent.current_speed.x:
                new_acc.x = agent.current_acc.x + self.acc_step
            elif agent.wanted_speed.x < agent.current_speed.x:
                new_acc.x = agent.current_acc.x - self.acc_step
            
            if agent.wanted_speed.y > agent.current_speed.y:
                new_acc.y = agent.current_acc.y + self.acc_step
            elif agent.wanted_speed.y < agent.current_speed.y:
                new_acc.y = agent.current_acc.y - self.acc_step
            
            if new_acc.x > 0:
                new_acc.x = min(self.max_acceleration, new_acc.x)
            else:
                new_acc.x = max(self.max_acceleration * -1, new_acc.x)
            if new_acc.y > 0:
                new_acc.y = min(self.max_acceleration, new_acc.y)
            else:
                new_acc.y = max(self.max_acceleration * -1, new_acc.y)

            old_speed = agent.current_speed
            new_speed = agent.current_speed + new_acc * self.time_interval

            new_positions.append(agent.current_coord + (old_speed + new_speed)/2.0)
            agent.current_speed = new_speed
            agent.current_acc = new_acc

        self.checkCollisions(new_positions)

        for pose, agent in zip(new_positions, self.agents):
            agent.current_coord = pose

        coords = self.getCoords()
        # updating data values
        x = [coord.x for coord in coords]
        y = [coord.y for coord in coords]
        self.agent_drawing.set_data(x,y)
        self.target_drawing.set_data(self.target.x, self.target.y)


        # This will run the GUI event
        # loop until all UI events
        # currently waiting have been processed
        self.fig.canvas.flush_events()

        time.sleep(self.time_interval)
        self.sim_time += self.time_interval
        plt.title("Alp's Simulator %.2f" % self.sim_time, fontsize=20)

    def updateTarget(self):
        target_update_rate = 0.1
        # from (1, 1) to (5, 1)
        if self.target_update_state == 0:
            if self.target == Point(5, 1):
                self.target_update_state = 1
                return    
            self.target.x += target_update_rate
        # from (5, 1) to (5, 5)
        elif self.target_update_state == 1:
            if self.target == Point(5, 5):
                self.target_update_state = 2
                return
            self.target.y += target_update_rate
        # from (5, 5) to (-5, 5)
        elif self.target_update_state == 2:
            if self.target == Point(-5, 5):
                self.target_update_state = 3
                return
            self.target.x -= target_update_rate
        # from (-5, 5) to (-5, -5)
        elif self.target_update_state == 3:
            if self.target == Point(-5, -5):
                self.target_update_state = 4
                return
            self.target.y -= target_update_rate
        # from (-5, -5) to (1, 1), initial position
        elif self.target_update_state == 4:
            if self.target == Point(1, 1):
                self.target_update_state = 0
                return
            self.target.x += target_update_rate
            self.target.y += target_update_rate
        else:
            print("You mixed something in target states!")
            exit(42)
        


    def getCoords(self):
        '''
        Returns a list of the current coordinates of all the agents in the swarm.
        
        :param self: the object that called the function
        :return: The current coordinates of each agent.
        '''
        return [agent.current_coord for agent in self.agents]


    def checkCollisions(self, positions):
        for i, pose1 in enumerate(positions):
            for j, pose2 in enumerate(positions[i + 1:]):
                dist = euDistance(pose1, pose2)
                if dist < self.collision_err_dist:
                    print("There is a collision between agent %d and %d." % (i, j+i+1))

                elif dist < self.collision_warn_dist:
                    print("Two agents are dangereously close, %d - %d" % (i, j+i+1))


    def close_signal_handler(self, sig, frame):
        '''
        When the user hits ctrl+C or ctrl+Z, the function close_signal_handler is called, which closes all figures
        and exits the program.
        
        :param sig: The signal number
        :param frame: the frame object that triggered the signal
        :return: None
        '''
        plt.close('all')
        sys.exit(0)

if __name__ == "__main__":
    x = None
    if len(sys.argv) == 1:
        with open("conf/example_data.json", "r") as f:
            x = json.load(f)
    else:
        parser = argparse.ArgumentParser(description='Swarm simulator')
        parser.add_argument("--mission",
                            metavar = "json_file",
                            type = str,
                            help = "json file for mission information" )
        parser.add_argument("--timeinterval",
                            metavar = "number",
                            type = float,
                            help = "time interval between steps")
        args = parser.parse_args()
        print("the data is ", args.mission)



    sim = Sim(4)

    while True:
        sim.step()