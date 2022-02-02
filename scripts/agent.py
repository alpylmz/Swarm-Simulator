from time import sleep
from helpers import Point, euDistance
from enum import Enum
from numpy import sign, isclose

class AlgoType(Enum):
    DEFAULT = 1
    SLIDING1 = 2
    SLIDING2 = 3

class Agent:
    def __init__(self, agent_num, coord, sim) -> None:
        '''
        The constructor of the class.
        
        :param self: the object itself
        :param agent_num: the number of the agent
        :param coord: the current coordinate of the agent
        :param sim: the simulation object
        :return: None
        '''
        self.agent_number = agent_num
        self.current_coord = coord
        self.sim = sim
        if self.agent_number % 2:
            self.current_speed = Point(0.01, 0.01)
        else:
            self.current_speed = Point(-0.01, -0.01)
        self.current_acc = Point(0., 0.)
        self.wanted_speed = Point(0., 0.)
        self.algorithm_type = AlgoType.SLIDING2
        self.attractive_constant = 0.5
        self.repulsive_constant = 0.9

    def set_speed(self, speed):
        '''
        Set the speed of the agent.
        
        :param self: This is a reference to the instance of the class
        :param speed: The speed you want to go at
        :return: None
        '''
        self.wanted_speed = speed

    ## FILL THIS FUNCTION FOR YOUR ALGORITHM
    def update(self):
        '''
        The function calculates the attractive and repulsive force for each agent and sums them up to get
        the current speed of each agent.
        
        :param self: the object itself
        :return: None
        '''
        aim = self.calcAimPoint()

        att_speed = self.calcAttractive(aim)
        rep_speed = self.calcRepulsive()

        if self.algorithm_type == AlgoType.DEFAULT:
            self.wanted_speed = att_speed * self.attractive_constant + rep_speed * self.repulsive_constant
        # assume u_o is (0.1,0.1)
        elif self.algorithm_type == AlgoType.SLIDING1:
            self.wanted_speed = att_speed * self.attractive_constant + rep_speed * self.repulsive_constant
            s_i = self.current_speed + self.wanted_speed * 10
            temp = Point(sign(s_i.x), sign(s_i.y))
            self.wanted_speed = temp * 0.2
        elif self.algorithm_type == AlgoType.SLIDING2:
            self.wanted_speed = att_speed * self.attractive_constant + rep_speed * self.repulsive_constant
        
            att_derivative = Point(-1, -1) * self.attractive_constant
            # since the repulsive force will not be used as long as there is a safe distance between agents,
            # I will not calculate repulsive force derivative for simplicity
            # I will assume that in any formation repulsive force will be (0, 0)
            rep_derivative = Point(0,0)

            #print("curr acc is ", str(self.current_acc))
            #s_derivative = self.current_acc + att_derivative
            s_derivative = self.current_acc + att_derivative
            
            boundary_val = 0.2 * self.sim.acc_for_interval
            if s_derivative.x < boundary_val and s_derivative.x > -boundary_val and s_derivative.y < boundary_val and s_derivative.y > -boundary_val:
                #print("deriv is close for agent %d" % self.agent_number, str(s_derivative)),
                #print("attractive part is ", str(att_derivative))
                #print("current acc is ", str(self.current_acc))
                return
            
            s_i = self.current_speed + self.wanted_speed * 100         
            self.wanted_speed = Point(sign(s_i.x)*0.1, sign(s_i.y)*0.1)

    def calcAimPoint(self):
        '''
        Calculate the aim point for the agent, given its number and the target location
        :return: The aim point for the UAV.
        '''
        if self.agent_number == 0:
            relative = Point(1,1)
        elif self.agent_number == 1:
            relative = Point(-1,-1)
        elif self.agent_number == 2:
            relative = Point(-1,1)
        elif self.agent_number == 3:
            relative = Point(1,-1)
        else:
            print("Aim is not defined for UAV %d!" % self.agent_number)
            exit(42)

        return relative + self.sim.target

        
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
        Calculate the repulsive force for a agent.
        
        :param self: the object that called the function
        :return: The speed of the agent.
        '''
        agentCoords = [agent.current_coord for agent in self.sim.agents if agent.agent_number != self.agent_number]
        return_speed = Point(0.0,0.0)
        for agent_coord in agentCoords:
            diff = Point(self.current_coord.x - agent_coord.x, self.current_coord.y - agent_coord.y)
            if diff.length() < 0.5:
                return_speed += 1/diff

        return return_speed

    # You need to fill this function if you want to benchmark your development with an observable value
    def calcError(self):
        '''
        Calculate the error between the current position and the aim point
        :return: The error between the current position and the aim position.
        '''
        aim = self.calcAimPoint()
        curr = self.current_coord
        return euDistance(aim, curr)
