import numpy as np 

class vec3:
    def __init__(self,x0: float, x1: float, x2: float):
        self.x0 = x0
        self.x1 = x1
        self.x2 = x2
    def __str__(self) -> str:
        return "[ {} {} {} ]".format(self.x0,self.x1,self.x2)
    def __add__(self,other):
        return  vec3(self.x0 + other.x0, self.x1 + other.x1, self.x2 + other.x2)
    def __iadd__(self,other):
        self.x0 = other.x0 + self.x0
        self.x1 = other.x1 + self.x1
        self.x2 = other.x2 + self.x2
        return self
    def __sub__(self,other):
        return vec3(self.x0 - other.x0, self.x1 - other.x1, self.x2 - other.x2)
    def __isub__(self,other):
        self.x0 = -other.x0 + self.x0
        self.x1 = -other.x1 + self.x1
        self.x2 = -other.x2 + self.x2
        return self
    def __mul__(self,other):
        if isinstance(other,vec3):
            return vec3(self.x0 * other.x0, self.x1 * other.x1, self.x2 * other.x2)
        elif isinstance(other,float) or isinstance(other,int) or isinstance(other,long):
            return vec3(self.x0 * other, self.x1 * other, self.x2 * other)
        else:
            assert(False,"cannot multiply vec3 by a non numeric class or non vec3")
    def __imul__(self,other):
        if isinstance(other,vec3):
            self.x0 = other.x0 * self.x0
            self.x1 = other.x1 * self.x1
            self.x2 = other.x2 * self.x2
            return self
        elif isinstance(other,float) or isinstance(other,int) or isinstance(other,long):
            self.x0 = x0 * other
            self.x1 = x1 * other
            self.x2 = x2 * other
            return self
        else:
            assert(False,"cannot multiply vec3 by a non numeric class or non vec3")
    def __truediv__(self,other):
        if isinstance(other,vec3):
            return vec3(self.x0 / other.x0, self.x1 / other.x1, self.x2 / other.x2)
        elif isinstance(other,float) or isinstance(other,int) or isinstance(other,long):
            return vec3(self.x0 / other, self.x1 / other, self.x2 / other)
        else:
            assert(False,"cannot divide vec3 by a non numeric class or non vec3")
    def __idiv__(self,other):
        if isinstance(other,vec3):
            self.x0 = self.x0 / other.x0 
            self.x1 = self.x1 / other.x1
            self.x2 = self.x2 / other.x2
            return self
        elif isinstance(other,float) or isinstance(other,int) or isinstance(other,long):
            self.x0 = x0 / other
            self.x1 = x1 / other
            self.x2 = x2 / other
            return self
        else: 
            assert(False,"cannot divide vec3 by a non numeric class or non vec3")
    def __neg__(self):
        return vec3(-self.x0,-self.x1,-self.x2)
    def __eq__(self,other):
        return ((self.x0 == other.x0) and (self.x1 == other.x1) and (self.x2 == other.x2))
    def __ne__(self,other):
        return not(self == other)
    def __pow__(self,other: float):
        return vec3(self.x0 ** other, self.x1 ** other,self.x2 ** other)
    def __ipow__(self,other: float):
        self.x0 = self.x0 ** other
        self.x1 = self.x1 ** other
        self.x2 = self.x2 ** other
        return self
    def __len__(self):
        return sqrt(self.x0 * self.x0 + self.x1 * self.x1 + self.x2 * self.x2)



