import sys
import math
from abc import ABC,abstractmethod
from geometry import * 
from material import *
import math 
import numpy as np 
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



#generate perlin noise
class perlin:
	def __init__(self,n: int = 256):
		self.ranfloat = np.random.rand(n)
		self.n = n
		self.perm_x = self.perm_gen()
		self.perm_y = self.perm_gen()
		self.perm_z = self.perm_gen()
	def perm_gen(self):
		p = np.arange(0,256,1)
		target = (np.random.rand(256) * np.arange(257,1,-1)).astype(np.int)
		# print(np.random.randn(256))
		for i in range(self.n):
			tmp = int(np.copy(p[i]))
			p[i],p[target[i]] = p[target[i]],tmp
		return p 
	def noise(self,p: vec3):
		u = p[0] - math.floor(p[0])
		v = p[1] - math.floor(p[1])
		w = p[2] - math.floor(p[2])
		i = int(4 * p[0]) & 255
		j = int(4 * p[1]) & 255
		k = int(4 * p[2]) & 255
		#print(self.ranfloat[ self.perm_x[i] ^ self.perm_y[j] ^ self.perm_z[k]])
		return self.ranfloat[ self.perm_x[i] ^ self.perm_y[j] ^ self.perm_z[k]]


class noise_texture(texture):
	def __init__(self):
		self.noise = perlin()
	def value(self,u: float, v: float, p: vec3):
		#print(self.noise.noise(p))
		return vec3(1,1,1) * self.noise.noise(p)


