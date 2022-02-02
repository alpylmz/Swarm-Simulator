from re import M
from time import sleep, time
from agent import Agent
from random import uniform
from helpers import Point, euDistance
from target_update import targetUpdate

import numpy as np
import time
import matplotlib.pyplot as plt
import sys
import signal
import json
import argparse
import random



class Sim:

    def __init__(self, agent_count, time_interval = 0.01, boundaries=[Point(0,0), Point(10,10)], plot_sim = False) -> None:
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
        self.acc_for_interval = 1/time_interval
        self.max_acceleration = 800.0
        self.max_jerk = 1.0
        self.max_jerk_for_time_interval = self.max_jerk / self.time_interval
        self.acc_step = 16000
        self.collision_warn_dist = 0.3
        self.collision_err_dist = 0.1

        self.error_boundary = 0.02
        self.plot_sim = plot_sim

        self.sim_time = 0.0

        # benchmark
        self.algorithm_error = 0.0
        self.dangerous_event_count = 0
        self.collision_count = 0

        self.agent_paths = []
        for i in range(self.agent_count):
            self.agent_paths.append([[],[]])


        # there are several paths that you can choose for target, number indicates that
        self.target_path_index = 2
        self.target_init = Point(1, 1)
        self.target = self.target_init
        self.target_path_x = [self.target.x]
        self.target_path_y = [self.target.y]
        self.target_update_state = 0

        self.coords = [agent.current_coord for agent in self.agents]

        if self.plot_sim:
            # to run GUI event loop
            plt.ion()

            # here we are creating sub plots
            self.fig = plt.figure()
            self.ax = self.fig.add_subplot(111)
            x = [coord.x for coord in self.coords]
            y = [coord.y for coord in self.coords]
            self.agent_drawing, = self.ax.plot(x,y,label='toto',color='b',marker='o',ls='')
            self.target_drawing, = self.ax.plot(self.target.x, self.target.y, color='r', marker='o')
            self.target_path_drawing, = self.ax.plot(self.target_path_x, self.target_path_y, color='r')

            self.agent_path_drawings = []
            for i in range(self.agent_count):
                self.agent_path_drawings.append(self.ax.plot(0,0, color = 'b'))

            self.fig.show()

            self.fig.canvas.mpl_connect('close_event', self._on_close)

            plt.xlim([-15, 15])
            plt.ylim([-15, 15])

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
        self.updateTarget()
        new_positions = []
        for index, agent in enumerate(self.agents):
            agent.update()

            new_acc = Point(0, 0)
            
            diff_x = agent.wanted_speed.x - agent.current_speed.x
            diff_x *= self.acc_for_interval
            if diff_x > 0:
                if diff_x > self.acc_step:
                    new_acc.x = agent.current_acc.x + self.acc_step
                else:
                    new_acc.x = diff_x

            elif diff_x < 0:
                if (diff_x * -1) < ( -1 * self.acc_step):
                    new_acc.x = agent.current_acc.x - self.acc_step
                else:
                    new_acc.x = diff_x

            diff_y = agent.wanted_speed.y - agent.current_speed.y
            diff_y *= self.acc_for_interval
            if diff_y > 0:
                if diff_y > self.acc_step:
                    new_acc.y = agent.current_acc.y + self.acc_step
                else:
                    new_acc.y = diff_y

            elif diff_y < 0:
                if (diff_y * -1) < (-1 * self.acc_step):
                    new_acc.y = agent.current_acc.y - self.acc_step
                else:
                    new_acc.y = diff_y
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

            new_pose = agent.current_coord + (old_speed + new_speed)/2.0
            new_positions.append(new_pose)
            self.agent_paths[index][0].append(new_pose.x)
            self.agent_paths[index][1].append(new_pose.y)
            agent.current_speed = new_speed
            self.agents[index].current_acc = new_acc

            #agent.current_acc = new_acc
            self.algorithm_error += agent.calcError()

        self.checkCollisions(new_positions)

        for pose, agent in zip(new_positions, self.agents):
            agent.current_coord = pose + Point(
                                        random.uniform(-1 * self.error_boundary, self.error_boundary),
                                        random.uniform(-1 * self.error_boundary, self.error_boundary))


        coords = self.getCoords()
        # updating data values
        x = [coord.x for coord in coords]
        y = [coord.y for coord in coords]

        if self.plot_sim:
            self.agent_drawing.set_data(x,y)
            self.target_drawing.set_data(self.target.x, self.target.y)
            
            self.target_path_x.append(self.target.x)
            self.target_path_y.append(self.target.y)
            self.target_path_drawing.set_data(self.target_path_x, self.target_path_y)

            for i in range(self.agent_count):
                self.agent_path_drawings[i][0].set_data(self.agent_paths[i][0], self.agent_paths[i][1])


            # This will run the GUI event
            # loop until all UI events
            # currently waiting have been processed
            self.fig.canvas.flush_events()
            plt.title("Alp's Simulator %.2f" % self.sim_time, fontsize=20)

            # there is no need to sleep if there is no plotting
            
            time.sleep(self.time_interval)
        self.sim_time += self.time_interval

    def updateTarget(self):
        target_update_rate = 0.1
        self.target, self.target_update_state = targetUpdate(target_update_rate, self.target_update_state, self.target, self.target_path_index)
        if self.target is None:
            # This if you want to end the simulation after one loop
            self._on_close(None)
            # This if you want to continue the simulation endlessly
            """
            self.target_update_state = 0
            self.target = self.target_init
            self.updateTarget()
            return
            """


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
                    self.collision_count += 1

                elif dist < self.collision_warn_dist:
                    print("Two agents are dangereously close, %d - %d" % (i, j+i+1))
                    self.dangerous_event_count += 1
                    

    def _on_close(self, event):
        '''
        The function is called when the user closes the GUI window
        
        :param event: the event that triggered the callback
        '''
        """
        ax = self.fig.add_subplot(111)
        self.target_path_drawing, = ax.plot(self.target_path_x, self.target_path_y, color='r')

        self.agent_path_drawings = []
        for i in range(self.agent_count):
            self.agent_path_drawings.append(ax.plot(0,0, color = 'b'))
        """

        if self.plot_sim:

            self.fig.clear()
            self.ax = self.fig.add_subplot(111)
            self.target_path_drawing, = self.ax.plot(self.target_path_x, self.target_path_y, color='r')
            self.target_path_drawing.set_data(self.target_path_x, self.target_path_y)

            self.agent_path_drawings = []
            for i in range(self.agent_count):
                self.agent_path_drawings.append(self.ax.plot(0,0, color = 'b'))

            for i in range(self.agent_count):
                self.agent_path_drawings[i][0].set_data(self.agent_paths[i][0], self.agent_paths[i][1])
            
            plt.xlim([-15, 15])
            plt.ylim([-15, 15])

            self.fig.canvas.flush_events()
            plt.show()

            plt.close('all')
        print("--------------------------------------------------")
        print("Simulation time is %.2f." % self.sim_time)
        print("The algorithms total error is %.2f." % self.algorithm_error)
        print("Average error is %.2f." % (self.algorithm_error/self.sim_time))
        print("--------------------------------------------------")
        print("Dangereous event count is %d." % self.dangerous_event_count)
        print("Collision count is %d." % self.collision_count)
        print("--------------------------------------------------")
        sys.exit(0)

    def close_signal_handler(self, sig, frame):
        '''
        When the user hits ctrl+C or ctrl+Z, the function close_signal_handler is called, which closes all figures
        and exits the program.
        
        :param sig: The signal number
        :param frame: the frame object that triggered the signal
        :return: None
        '''
        if self.plot_sim:
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