import sys
import math
from abc import ABC,abstractmethod
import random 
class sampler(ABC):
	# initialize your sampler based on its specific properties
	def __init__(self, nx: float, ny: float,seed: float):
		pass 
	# all samplers should take an input coordinate and generate a u,v pixel coordinate
	def generate_sample_uv(self,i: int, j: int):
		return (0.0,0.0);

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