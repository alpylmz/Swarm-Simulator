from time import sleep
from helpers import Point, euDistance
from enum import Enum
from numpy import diff, sign, isclose, sqrt

class AlgoType(Enum):
    DEFAULT = 1
    SLIDING1 = 2
    SLIDING2 = 3
    STATE1 = 4
    SLIDINGSTATE = 5

class Machine1State(Enum):
    NOT_IN_FORMATION = 1
    IN_FORMATION = 2
    BROKEN_FORMATION = 3

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
        self.algorithm_type = AlgoType.SLIDINGSTATE
        self.machine_state = Machine1State.NOT_IN_FORMATION
        self.attractive_constant = 0.5
        self.repulsive_constant = 0.7
        self.max_speed = 0.1

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
        rep_speed_agents = self.calcRepulsiveAgents()
        rep_speed_obstacles = self.calcRepulsiveObstacles()
        if rep_speed_obstacles is False:
            return False
        rep_speed = rep_speed_agents + rep_speed_obstacles


        if self.algorithm_type == AlgoType.DEFAULT:
            self.wanted_speed = att_speed * self.attractive_constant + rep_speed * self.repulsive_constant
            if self.wanted_speed.length() > 1:
                self.wanted_speed /= self.wanted_speed.length()
                self.wanted_speed /= 10
        # assume u_o is (0.1,0.1)
        elif self.algorithm_type == AlgoType.SLIDING1:
            self.wanted_speed = att_speed * self.attractive_constant + rep_speed * self.repulsive_constant
            s_i = self.current_speed + self.wanted_speed * 10
            temp = Point(sign(s_i.x), sign(s_i.y))
            self.wanted_speed = temp * 0.2
            if self.wanted_speed.length() > 1:
                self.wanted_speed /= self.wanted_speed.length()
                self.wanted_speed /= 10
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
                self.wanted_speed /= self.wanted_speed.length()
                self.wanted_speed /= 5
                return
            
            s_i = self.current_speed + self.wanted_speed * 100         
            self.wanted_speed = Point(sign(s_i.x)*0.1, sign(s_i.y)*0.1)

            if self.wanted_speed.length() > 1:
                self.wanted_speed /= self.wanted_speed.length()
                self.wanted_speed /= 10

        elif self.algorithm_type == AlgoType.STATE1:
            # state transitions
            epsilon_for_dist = 0.5
            dist = euDistance(aim, self.current_coord)
            if self.machine_state == Machine1State.NOT_IN_FORMATION:
                if dist < epsilon_for_dist:
                    #print("state changed to information %d" % self.agent_number)
                    self.machine_state = Machine1State.IN_FORMATION
            
            elif self.machine_state == Machine1State.IN_FORMATION:
                if dist > epsilon_for_dist:
                    #print("state changed to notinformed %d" % self.agent_number)
                    self.machine_state = Machine1State.BROKEN_FORMATION

            elif self.machine_state == Machine1State.BROKEN_FORMATION:
                if dist < epsilon_for_dist:
                    self.machine_state = Machine1State.IN_FORMATION

            # things that will be changed by state
            attractive_constant = None
            repulsive_constant = None
            if self.machine_state == Machine1State.NOT_IN_FORMATION:
                attractive_constant = self.attractive_constant * 2
                repulsive_constant = self.repulsive_constant
            elif self.machine_state == Machine1State.BROKEN_FORMATION:
                attractive_constant = self.attractive_constant * 2
                repulsive_constant = self.repulsive_constant
            elif self.machine_state == Machine1State.IN_FORMATION:
                attractive_constant = self.attractive_constant
                repulsive_constant = self.repulsive_constant

            self.wanted_speed = att_speed * attractive_constant + rep_speed * repulsive_constant

            att_derivative = Point(-1, -1) * attractive_constant
            s_derivative = self.current_acc + att_derivative
            
            boundary_val = 0.2 * self.sim.acc_for_interval
            if s_derivative.x < boundary_val and s_derivative.x > -boundary_val and s_derivative.y < boundary_val and s_derivative.y > -boundary_val:
                #print("deriv is close for agent %d" % self.agent_number, str(s_derivative)),
                #print("attractive part is ", str(att_derivative))
                #print("current acc is ", str(self.current_acc))
                if self.machine_state == Machine1State.NOT_IN_FORMATION:
                    self.wanted_speed /= self.wanted_speed.length()
                    self.wanted_speed /= 4
                elif self.machine_state == Machine1State.BROKEN_FORMATION:
                    self.wanted_speed /= self.wanted_speed.length()
                    self.wanted_speed /= 2
                    #print("broken", self.wanted_speed)
                elif self.machine_state == Machine1State.IN_FORMATION:
                    # just some constant number for now
                    if rep_speed.length() > 3:
                        self.wanted_speed = rep_speed * repulsive_constant * 0.1
                    pass
                return
            
            if self.machine_state == Machine1State.NOT_IN_FORMATION or self.machine_state == Machine1State.BROKEN_FORMATION:
                s_i = self.current_speed + self.wanted_speed * 100         
                self.wanted_speed = Point(sign(s_i.x)*0.1, sign(s_i.y)*0.1)

        elif self.algorithm_type == AlgoType.SLIDINGSTATE:
            lie_deriv1 = Point(0, 0)
            lie_deriv2 = Point(0, 0)
            current_position = self.current_coord

            # atttractive potential field is
            # att = (eucDistance(aim - current_position))^2 
            attractive_potential1 = (euDistance(aim, current_position) ** 4)
            attractive_speed1 = aim - current_position
            attractive_speed1 /= attractive_speed1.length()
            attractive_speed1 *= 0.01
            temp_position = current_position + attractive_speed1
            attractive_potential2 = (euDistance(aim, temp_position) ** 4)
            attractive_derivative = (attractive_potential2 - attractive_potential1) / 0.01

            # repulsive potential field is
            # rep = (eucDistance(current_position - other_agents_positions))^2
            repulsive_potential1 = 0
            repulsive_speed = Point(0, 0)
            agentCoords = [agent.current_coord for agent in self.sim.agents if agent.agent_number != self.agent_number]
            for agent in agentCoords:
                repulsive_potential1 += (euDistance(agent, current_position) ** 2) * 0.01
                repulsive_speed = 1/(current_position - agent)
            repulsive_speed /= repulsive_speed.length()
            repulsive_speed *= 0.01
            temp_position = current_position + repulsive_speed
            repulsive_potential2 = 0
            for agent in agentCoords:
                repulsive_potential2 += (euDistance(agent, temp_position) ** 2)
            repulsive_derivative = (repulsive_potential2 - repulsive_potential1) / 0.01

            lie_deriv1 = attractive_derivative
            lie_deriv2 = repulsive_derivative

            # now calculate the speed by using lie_deriv1 and lie_deriv2 with sliding mode control
            self.wanted_speed = 1 / (lie_deriv2 - lie_deriv1) * (lie_deriv2 * attractive_speed1 - lie_deriv1 * repulsive_speed)
            if euDistance(aim, current_position) > 0.3:
                self.wanted_speed *= 30
            elif euDistance(aim, current_position) > 0.2:
                self.wanted_speed *= 10

    
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

    def calcRepulsiveAgents(self):
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

    def calcRepulsiveObstacles(self):
        return_speed = Point(0.0, 0.0)
        for obstacle in self.sim.obstacles:
            center = obstacle[0]
            r = obstacle[1]
            center_distance = euDistance(center, self.current_coord)
            circle_distance = center_distance - r
            if circle_distance < 0:
                print("Inside of obstacle!")
                return False
            if circle_distance < 1:
                dist = self.current_coord + center * -1
                dist.x -= r
                dist.y -= r
                return_speed += 1/dist
        
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
