from math import sqrt
class Point:
    # constructed using a normal tupple
    def __init__(self, point_t = (0,0)):
        self.x = float(point_t[0])
        self.y = float(point_t[1])

    # define all useful operators
    def __add__(self, other):
        return Point((self.x + other.x, self.y + other.y))
    def __sub__(self, other):
        return Point((self.x - other.x, self.y - other.y))
    def __mul__(self, scalar):
        return Point((self.x*scalar, self.y*scalar))
    def __div__(self, scalar):
        return Point((self.x/scalar, self.y/scalar))
    def __len__(self):
        return int(sqrt(self.x**2 + self.y**2))
    # get back values in original tuple format
    def mul(self,other):
        return Point((self.x*other.x,self.y*other.y))

    def div(self,other):
        return Point((self.x/other.x,self.y/other.y))
    def get(self, neg = False):
        if neg:
            return (- self.x, - self.y)

        return (self.x, self.y)