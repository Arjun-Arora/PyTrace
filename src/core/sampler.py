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

'''
uniform sampler

nx: num x pixels
ny: num y pixels
seed: random seed value

'''
class uniform_sampler(sampler):
	def __init__(self,nx: float, ny: float, seed: float = None):
		if seed is not None:
			random.seed(seed)
		self.nx = nx
		self.ny = ny 
	def generate_sample_uv(self,i: int, j: int): 
		u = (i + random.random())/self.nx
		v = (j + random.random())/self.ny
		return u,v 
	def generate_n_samples_uv(self,i: int, j: int,num_samples: int):
		samples = []
		for k in range(num_samples):
			samples.append(self.generate_sample_uv(i,j))
		return samples



'''
stratified sampler

N is square of the number of stratified samples per x,y dimension
'''
class stratified_sampler(sampler):
	def __init__(self,nx: float, ny: float,N: int, seed: float = None): 
		sqrt_N = int(math.sqrt(N))
		self.s = self.t = sqrt_N

