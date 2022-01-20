from math import sqrt


class Point:
    def __init__(self, x, y) -> None:
        '''
        Create a new object of type Point with x and y attributes.
        
        :param self: This is a reference to the current instance of the class
        :param x: The x coordinate of the point
        :param y: the y-coordinate of the point
        :return: None
        '''
        self.x = x
        self.y = y

    def __add__(self, o):
        '''
        Add two points together.
        
        :param self: This is a reference to the current instance of the class
        :param o: the object to be added to the current object
        :return: A new Point object.
        '''
        return Point(self.x + o.x, 
                     self.y + o.y)

    def __mul__(self, o):
        '''
        multiply the point by a scalar.
        
        :param self: This is a reference to the current instance of the class
        :param o: the object to multiply by
        :return: A new Point object.
        '''
        return Point(self.x * o,
                     self.y * o)

    def __rmul__(self, o):
        '''
        multiply the Point by a scalar.
        
        :param self: This is a reference to the current instance of the class
        :param o: the object on the right side of the *
        :return: A Point object.
        '''
        return Point(self.x * o,
                     self.y * o)

    def __truediv__(self, o):
        '''
        Create a new Point object that is the result of dividing the current Point object by a scalar.
        
        :param self: This is a reference to the current instance of the class
        :param o: the object to be divided
        :return: A new Point object.
        '''
        return Point(self.x / o,
                     self.y / o)

    def __rtruediv__(self, o):
        '''
        Return a Point object whose coordinates are the reciprocals of the coordinates of the Point
        object on which the function is called.
        
        :param self: This is a reference to the object that is calling the method
        :param o: the object on the right side of the operator
        :return: A Point object.
        '''
        return Point(o / self.x,
                     o / self.y)

    def length(self):
        '''
        Return the length of the vector.
        
        :param self: This is a reference to the object that is calling the method
        :return: The length of the vector.
        '''
        return sqrt(self.x**2 + self.y**2)

def euDistance(point1, point2):
    '''
    Compute the Euclidean distance between two points.
    
    :param point1: the first point
    :param point2: the point to which the distance is calculated
    :return: The distance between the two points.
    '''
    return sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

