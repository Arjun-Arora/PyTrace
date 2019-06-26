import numpy as np
from abc import ABC,abstractmethod
from utils import * 
from ray import * 
import sys
MAX_FLOAT = sys.float_info.max

class hit_record:
	def __init__(self,t: np.ndarray,p: np.ndarray, normal: np.ndarray):
		'''
		t: tile of distances along rays to tile hit (m x n x 1) (non-hits == -1.0)
		p: location in worldspace of what rays in tile hit (m x n x 3)
		normal: normals created from hits in tile
		'''
		self.t = t
		self.p = p
		self.normal = normal

class hitable(ABC):
	def __init__(self):
		pass
	def hit(self,r: ray,t_min: np.ndarray ,t_max: np.ndarray):
		'''
		t_min: tile of minimum values along rays to hit (m x n x 1)
		t_min: tile of max values along rays to hit (m x n x 1)
		r: ray tile

		'''
		pass

def iterate_hit_list(r:ray, t_min:float, t_max: float, object_list: list):
	rec = None
	hit_anything = False
	closest_hit = t_max
	rec_list = []
	#print(len(object_list))
	for i in range(0,len(object_list)):
		#print(i)
		hit_object,temp_rec = object_list[i].hit(r,t_min,closest_hit)
		#print("normal: {},i : {}".format(temp_rec.normal,i))
		if hit_object:
			#print("hit this")
			hit_anything = True
			closest_hit = np.minimum(np.where(temp_rec.t > 0,temp_rec.t,MAX_FLOAT),closest_hit)
			#print(np.unique(closest_hit))
			rec_list.append(temp_rec)
	return hit_anything,rec_list

