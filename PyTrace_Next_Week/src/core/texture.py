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

def trilinear_interp(c: np.array, u: float, v: float, w: float):
	accum = 0
	for i in range(2):
		for j in range(2):
			for k in range(2):
				accum += (i * u + (1 - i) * (1 - u)) * \
						 (j * v + (1 - j) * (1 - v)) * \
						 (k * w + (1 - k) * (1 - w)) * c[i,j,k]
	return accum

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

		u *= u * (3 - 2*u)
		v *= v * (3 - 2*v)
		w *= w * (3 - 2*w)

		i = int(math.floor(p[0]))
		j = int(math.floor(p[1]))
		k = int(math.floor(p[2]))

		c = np.zeros((2,2,2))
		for di in range(2):
			for dj in range(2):
				for dk in range(2):
					c[di,dj,dk] = self.ranfloat[ self.perm_x[(i + di) & 255] ^ self.perm_y[(j + dj) & 255] ^ self.perm_z[(k + dk) & 255]]
		return trilinear_interp(c,u,v,w)


class noise_texture(texture):
	def __init__(self,scale: int = 1):
		self.noise = perlin()
		self.scale = scale
	def value(self,u: float, v: float, p: vec3):
		#print(self.noise.noise(p))
		return vec3(1,1,1) * self.noise.noise(self.scale * p)


