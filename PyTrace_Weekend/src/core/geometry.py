import numpy as np 

class vec3:
    def __init__(self,x0: float, x1: float, x2: float):
        self.x0 = x0
        self.x1 = x1
        self.x2 = x2
        self.x = x0
        self.y = x1
        self.z = x2

        self.r = x0
        self.g = x1
        self.b = x2
    def __str__(self) -> str:
        return "[ {} {} {} ]".format(self.x0,self.x1,self.x2)
    def __add__(self,other):
        return  vec3(self.x0 + other.x0, self.x1 + other.x1, self.x2 + other.x2)
    def __sub__(self,other):
        return vec3(self.x0 - other.x0, self.x1 - other.x1, self.x2 - other.x2)



