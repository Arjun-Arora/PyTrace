import sys
import math
from abc import ABC,abstractmethod
import random 
import numpy as np 
class sampler(ABC):
	# initialize your sampler based on its specific properties
	def __init__(self, nx: float, ny: float,seed: float):
		pass 
	# all samplers should take an input coordinate and generate a u,v pixel coordinate
	def generate_sample_uv(self,i: int, j: int):
		return (0.0,0.0);

def is_square(integer):
	root = math.sqrt(integer)
	return integer == int(root + 0.5) ** 2

'''
uniform sampler

nx: num x pixels
ny: num y pixels
seed: random seed value

'''
class uniform_sampler(sampler):
	def __init__(self, seed: float = None):
		if seed is not None:
			random.seed(seed)
	def generate_sample_uv(self): 
		u = (random.random())
		v = (random.random())
		return u,v 
	def generate_n_samples_uv(self,i: int, j: int,num_samples: int):
		samples = []
		for k in range(num_samples):
			samples.append(self.generate_sample_uv())
		return samples



'''
stratified sampler

N is square of the number of stratified samples per x,y dimension
'''
class stratified_sampler(sampler):
	def __init__(self,N: int, seed: float = None): 
		assert is_square(N),"For stratified sampler,N must be a square number"
		if seed is not None:
			random.seed(seed)
		self.sqrt_N = int(math.sqrt(N))
	def generate_sample_uv(self,s: int,t: int):
		u = (s + random.random())/(self.sqrt_N)
		v = (t + random.random())/(self.sqrt_N)
		return u,v
	def generate_n_samples_uv(self,i: int, j: int,num_samples: int):
		samples = []
		for s in range(self.sqrt_N):
			for t in range(self.sqrt_N):
				samples.append(self.generate_sample_uv(s,t))
		return samples



