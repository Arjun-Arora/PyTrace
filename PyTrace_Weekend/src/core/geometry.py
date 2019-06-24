import numpy as np 
import math
from typing import Type

class vec3:
    def __init__(self,x0: float, x1: float, x2: float):
        self.x0 = x0
        self.x1 = x1
        self.x2 = x2
    def x(self):
        return self.x0
    def y(self):
        return self.x1
    def z(self):
        return self.x2
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
    def __rmul__(self,other):
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
            self.x0 = self * other
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
            self = self / other
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
    def __getitem__(self,key):
        #assert( (key <= 2 and key >= 0), "key values must be between 0 and 2")
        if key == 0:
            return self.x0
        elif key == 1:
            return self.x1
        elif key == 2: 
            return self.x2
    def __setitem__(self,key,value):
        #assert( (key <= 2 and key >= 0), "key values must be between 0 and 2")
        if key == 0:
            self.x0 = value
        elif key == 1: 
            self.x1 = value
        elif key == 2:
            self.x2 = value

    def length(self):
        return np.sqrt(self.x0 * self.x0 + self.x1 * self.x1 + self.x2 * self.x2)
    def squared_length(self):
        return self.x0 * self.x0 + self.x1 * self.x1 + self.x2 * self.x2
    def dot(self,other):
        return self.x0 * other.x0 + self.x1 * other.x1 + self.x2 * other.x2
    def cross(self,other):
        return vec3(self.x1*other.x2 - self.x2 * other.x1,
                    -(self.x0*other.x2 - self.x2 * other.x0),
                      self.x0 * other.x1 - self.x1 * other.x0)
    def normalize(self):
        length = self.length()
        self.x0 = self.x0/length
        self.x1 = self.x1/length
        self.x2 = self.x2/length
        return self
def unit_vector(vec: vec3):
    return vec/vec.length()

class ray:
    def __init__(self,a: vec3, b: vec3):
        self.a = a
        self.b = b
    def origin(self):
        return self.a
    def direction(self):
        return self.b
    def __call__(self,t):
        return self.a + (t * self.b)

class rayTile: 
    def __init__(self,originTile: np.array,directionTile: np.array):
        # originTile: m,n,3
        # directionTile: m,n,3
        self.originTile = originTile
        self.directionTile = directionTile
        def originTile(self):
            return self.originTile
        def direction(self):
            return self.directionTile
        def __call__(self,t: float):
            return self.originTile + (t * self.directionTile)

