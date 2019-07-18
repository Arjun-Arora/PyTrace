import sys
import math
from abc import ABC,abstractmethod
from geometry import * 
from material import *


'''
replacement for hit_record struct 
'''
class hit_record:
	def __init__(self,t: float = 0.0,p_vec: vec3 = vec3(0,0,0),normal: vec3 = vec3(0,0,0),mat = None):
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
	def bounding_box(self, t0: float, t1: float):
		pass

def ffmin(a: float, b: float):
	return (b,a )[a < b]
def ffmax(a: float, b: float):
	return (b,a)[a > b]


class aabb:
	def __init__(self,a: vec3, b: vec3):
		self._min = a;
		self._max = b; 
	def hit(self,r: ray, tmin: float, tmax: float):
		for a in range(0,3):
			invD = 1.0/r.direction[a]
			t0 = (self._min[a] - r.origin[a]) * invD
			t1 = (self._max[a] - r.origin[a]) * invD
			if (invD < 0.0):
				t0,t1 = t1,t0
			tmin = (tmin,t0)[t0 > tmin]
			tmax = (tmax,t1)[t1 < tmax]
			if (tmax <= tmin):
				return False;
		return True

def sorrounding_box(box0: aabb, box1: aabb): 
	 small = vec3(ffmin(box0._min[0],box1._min[0]),
	 			  ffmin(box0._min[1],box1._min[1]),
	 			  ffmin(box0._min[2],box1._min[2]))
	 big = vec3(ffmax(box0._max[0],box1._max[0]),
	 			ffmax(box0._max[1],box1._max[1]),
	 			ffmax(box0._max[2],box1._max[2]))
	 return aabb(small,big)



'''
substitute function for hitable_list 
since list in python can already deal with abritrary classes and we dont need to specify a
special class to store lists and the hit functionality.

Here we just iterate through a list of hitable objects and record the closest hit for any ray

'''
class hitable_list(hitable):
	def __init__(self,object_list: list):
		self.object_list = object_list
	def hit(self,r:ray, t_min:float, t_max: float):
		rec = hit_record()
		hit_anything = False
		closest_hit = t_max
		idx = 0
		for i in range(0,len(self.object_list)):
			hit_object,temp_rec = self.object_list[i].hit(r,t_min,closest_hit)
			#print("normal: {},i : {}".format(temp_rec.normal,i))
			if hit_object:
				idx = i
				hit_anything = True
				closest_hit = temp_rec.t
				rec = temp_rec
		return hit_anything,rec
	def bounding_box(self, t0: float, t1: float):
		temp_box = None 
		box = None 
		if (len(self.object_list) < 1 ): return (False,box)

		first_true,temp_box = self.object_list[0].bounding_box(t0,t1)
		if (not first_true):
			return (False,box)
		else:
			box = temp_box
		for i in range(len(self.object_list)):
			check,temp_box = self.object_list[i].bounding_box(t0,t1)
			if check:
				box = sorrounding_box(box,temp_box)
			else: 
				return (False,box)
		return (True,box)


class bvh_node(hitable):
	def __init__(self,object_list,time0: float,time1: float):
		self.object_list = object_list
		self.time0 = time0
		self.time1 = time1
		self.left = None
		self.right = None 
		self.box = None
	def bounding_box(self):
		return (True,self.box)
	def hit(self,r:ray, t_min:float, t_max: float):
		rec = hit_record()
		if self.box.hit(r,t_min,t_max):
			left_rec = hit_record()
			right_rec = hit_record()
			hit_left,left_rec = self.left.hit(r,t_min,t_max)
			hit_right,right_rec = self.right.hit(r,t_min,t_max)
		else:
			return (False,rec)


