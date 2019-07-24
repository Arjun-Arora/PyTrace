import sys
import math
from abc import ABC,abstractmethod
from geometry import * 
from material import *
import math 
import numpy as np 
from noise import pnoise3
# abstract texture base class
class texture(ABC):
	def __init__(self):
		pass
	def value(u: float, v: float, p: vec3):
		pass 

class constant_texture(texture): 
	def __init__(self, color: vec3):
		self.color = color
	def value(self, u: float, v: float, p: vec3):
		return self.color

class checker_texture(texture):
	def __init__(self, texture1: texture, texture2: texture):
		self.even,self.odd = texture1,texture2
	def value(self,u: float, v: float, p: vec3):
		sines = float(math.sin(10 * p[0]) * math.sin(10 * p[1]) * math.sin(10 * p[2]))
		if sines < 0: 
			return self.odd.value(u,v,p)
		else:
			return self.even.value(u,v,p)
			

#use perlin noise generator to generate noise
class noise_texture(texture):
	def __init__(self,scale: int = 1):
		self.scale = scale
	def value(self,u: float, v: float, p: vec3):
		#print(self.noise.noise(p))
		p = self.scale * p
		rescale_perlin = (pnoise3(p[0],p[1],p[2]) +1)/(2)
		return_val = vec3(1,1,1) * rescale_perlin
		#print(return_val)
		return return_val


