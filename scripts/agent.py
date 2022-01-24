from helpers import Point, euDistance


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
        self.current_acc = Point(0.0, 0.0)
        self.wanted_speed = Point(0.01, 0.01)

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
        aim = Point(1,1)
        if self.agent_number == 0:
            aim = Point(2,2)
        elif self.agent_number == 1:
            aim = Point(2,0)
        elif self.agent_number == 2:
            aim = Point(0,2)
        elif self.agent_number == 3:
            aim = Point(0,0)
        elif self.agent_number == 4:
            aim = Point(1,1)

        att_speed = self.calcAttractive(aim)
        rep_speed = self.calcRepulsive()

        self.wanted_speed = att_speed * 0.1 + rep_speed * 0.4
        
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
