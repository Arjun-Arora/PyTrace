import numpy as np 
import math
from typing import Type

class vec3:
    def __init__(self,x0: float, x1: float, x2: float):
        self.arr = np.array([x0,x1,x2]).astype(float)
    def x(self): return self.arr[0]
    def y(self): return self.arr[1]
    def z(self): return self.arr[2]
    def r(self): return self.arr[0]
    def g(self): return self.arr[1]
    def b(self): return self.arr[2]
    def __str__(self) -> str:
        return str(self.arr)
    def __add__(self,other):
        return  vec3(self.x() + other.x(), self.y() + other.y(), self.z() + other.z())
    def __iadd__(self,other):

        self.arr  += other.arr
        return self
    def __sub__(self,other):
        return vec3(self.x() - other.x(), self.y() - other.y(), self.z() - other.z())
    def __isub__(self,other):
        self.arr  -= other.arr 
        return self
    def __mul__(self,other):
        if isinstance(other,vec3):
            return vec3(self.x() * other.x(), self.y() * other.y(), self.z() * other.z())
        else:
            return vec3(self.x() * other, self.y() * other, self.z() * other)
    def __rmul__(self,other):
        if isinstance(other,vec3):
            return vec3(self.x() * other.x(), self.y() * other.y(), self.z() * other.z())
        else:
            return vec3(self.x() * other, self.y() * other, self.z() * other)

    def __imul__(self,other):
        if isinstance(other,vec3):
            self.arr  *= other.arr
            return self
        else:
            self.arr *= other
            return self
    def __truediv__(self,other):
        if isinstance(other,vec3):
            return vec3(self.x() / other.x(), self.y() / other.y(), self.z() / other.z())
        else:
            return vec3(self.x() / other, self.y() / other, self.z() / other)
    def __idiv__(self,other):
        if isinstance(other,vec3):
            self.arr /= other.arr
            return self
        else:
            self = self / other
            return self

    def __neg__(self):
        return vec3(-self.x(),-self.y(),-self.z())
    def __eq__(self,other):
        return ((self.x() == other.x()) and (self.y() == other.y()) and (self.z() == other.z()))
    def __ne__(self,other):
        return not(self == other)
    def __pow__(self,other: float):
        return vec3(self.x() ** other, self.y() ** other,self.z() ** other)
    def __ipow__(self,other: float):
        self.arr = np.array([self.x() ** other,self.y() ** other,self.z() ** other])
        return self
    def __getitem__(self,key):
        #assert( (key <= 2 and key >= 0), "key values must be between 0 and 2")
        return self.arr[key]
    def __setitem__(self,key,value):
        #assert( (key <= 2 and key >= 0), "key values must be between 0 and 2")
        self.arr[key] = value

    def length(self):
        return np.sqrt(self.x() ** 2 + self.y() ** 2 + self.z() ** 2)
    def squared_length(self):
        return self.x() ** 2 + self.y() ** 2 + self.z() ** 2
    def dot(self,other):
        return self.arr.dot(other.arr)
    def cross(self,other):
        new_arr = np.cross(self.arr,other.arr)
        return vec3(new_arr[0],new_arr[1],new_arr[2])
    def normalize(self):
        self.arr /= self.length()
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

