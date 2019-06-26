import numpy as np
from utils import * 
from ray import * 
import sys

class camera:
	def __init__(self):
		self.lower_left_corner = vec3(-2.0,-1.0,-1.0)
		self.horizontal = vec3(4.0,0,0)
		self.vertical = vec3(0.0,2,0)
		self.origin = vec3(0.0,0.0,0.0)
	def get_ray(self,u: np.ndarray, v: np.ndarray):
		return ray(self.origin,self.lower_left_corner + u * self.horizontal + v * self.vertical)