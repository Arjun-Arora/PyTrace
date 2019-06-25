import sys
import math
from abc import ABC,abstractmethod
from geometry import * 
from material import *

'''
replacement for hit_record struct 
'''
class hit_record:
	def __init__(self,t: float = 0.0,p_vec: vec3 = vec3((0,0,0)),normal: vec3 = vec3((0,0,0)),mat: material = None):
		self.t = t
		self.p = p_vec
		self.normal = normal
		self.mat = mat
class hitable(ABC):
	def __init__(self,r: ray,t_min: float ,t_max: float):
		self.r = r
		self.t_min = t_min
		self.t_max = t_max
		self.rec = rec
	def hit(self):
		pass
'''
substitute function for hitable_list 
since list in python can already deal with abritrary classes and we dont need to specify a
special class to store lists and the hit functionality.

Here we just iterate through a list of hitable objects and record the closest hit for any ray
'''
def iterate_hit_list(r:ray, t_min:float, t_max: float, object_list: list):
	rec = hit_record()
	hit_anything = False
	closest_hit = t_max
	idx = 0
	for i in range(0,len(object_list)):
		hit_object,temp_rec = object_list[i].hit(r,t_min,closest_hit)
		#print("normal: {},i : {}".format(temp_rec.normal,i))
		if hit_object:
			idx = i
			hit_anything = True
			closest_hit = temp_rec.t
			rec = temp_rec
	return hit_anything,rec


