import sys
import math
from abc import ABC,abstractmethod
from geometry import * 
class hit_record:
	def __init__(self,t: float = 0.0,p_vec: vec3 = vec3(0,0,0),normal: vec3 = vec3(0,0,0)):
		self.t = t
		self.p = p_vec
		self.normal = normal
class hitable(ABC):
	def __init__(self,r: ray,t_min: float ,t_max: float):
		self.r = r
		self.t_min = t_min
		self.t_max = t_max
		self.rec = rec
	def hit(self):
		pass

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


# class hitable_list(hitable):
# 	def __init__(self,list_l: list, n: int):
# 		self.hit_list = list_l
# 		self.list_size = n
# 	def hit(self,r: ray, t_min: float ,t_max: float ,rec: hit_record):
# 		temp_rec = hit_record()
# 		hit_anything = False
# 		closest_hit = t_max
# 		for i in range(0,self.list_size):
# 			# print(self.hit_list)
# 			hit_anything,temp_rec = self.hit_list[i].hit(r,t_min,closest_hit,temp_rec)
# 			if (hit_anything):
# 				hit_anything = True
# 				closest_hit = temp_rec.t
# 				rec = temp_rec
# 		return hit_anything,rec

