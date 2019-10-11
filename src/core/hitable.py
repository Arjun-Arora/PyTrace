import sys
import math
from abc import ABC,abstractmethod
from geometry import * 
from material import *
from math import pi,sin,cos
FLT_MAX = sys.float_info.max
import copy 
sys.setrecursionlimit(1500)

'''
replacement for hit_record struct 
'''
class hit_record:
	def __init__(self,t: float = 0.0,p_vec: vec3 = vec3(0,0,0),
					 normal: vec3 = vec3(0,0,0),mat = None,
					 u: float = 0.0,v:float = 0.0):
		self.t = t
		self.p = p_vec
		self.normal = normal
		self.mat = mat
		self.u = u
		self.v = v 
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
since list in python can already deal with abritrary objects and we dont need to specify a
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

#returns x,y or z value of hitable to sort bvh depending on axis 
def box_x_val(a: hitable):
	check,box = a.bounding_box(0,0)
	if not check:
		assert(False)
	return box._min[0]
def box_y_val(a: hitable):
	check,box = a.bounding_box(0,0)
	if not check:
		assert(False)
	return box._min[1]
def box_z_val(a: hitable):
	check,box = a.bounding_box(0,0)
	if not check:
		assert(False)
	return box._min[2]

'''
bounding volume hierarchy node 
'''
class bvh_node(hitable):
	def __init__(self,object_list,time0: float,time1: float):
		self.object_list = object_list
		self.time0 = time0
		self.time1 = time1
		self.left = None
		self.right = None 
		self.box = None
		# print(len(self.object_list))

		axis = int(random.random() * 3)
		if axis == 0:
			sorted(self.object_list,key = box_x_val)
		elif axis == 1: 
			sorted(self.object_list,key = box_y_val)
		elif axis == 2: 
			sorted(self.object_list,key = box_z_val)

		if len(self.object_list) == 1:
			#print('hit here')
			self.left = self.object_list[0]
			self.right = self.left
		elif len(self.object_list) == 2: 
			self.left = self.object_list[0]
			self.right = self.object_list[1]
		else: 
			n = len(self.object_list)
			split = int(n/2)
			#print(split)
			# print("went left")
			self.left = bvh_node(self.object_list[:split],self.time0,self.time1)
			# print('went right')
			# print("split: {}  n - split: {}".format(split,n - split) )
			if split != n - split:
				self.right =bvh_node(self.object_list[split: n - split],self.time0,self.time1)
			else: 
				self.right = bvh_node(self.object_list[split:],self.time0,self.time1)

		left_check,left_box = self.left.bounding_box(self.time0,self.time1)
		right_check,right_box = self.right.bounding_box(self.time0,self.time1)
		if not left_check or not right_check:
			assert(False, "missing bounding box in bvh node construction")
		self.box = sorrounding_box(left_box,right_box)
		
	def bounding_box(self,t0: float, t1: float):
		return (True,self.box)
	def hit(self,r:ray, t_min:float, t_max: float):
		rec = hit_record()
		if self.box.hit(r,t_min,t_max):
			left_rec = hit_record()
			right_rec = hit_record()
			hit_left,left_rec = self.left.hit(r,t_min,t_max)
			hit_right,right_rec = self.right.hit(r,t_min,t_max)
			if(hit_left and hit_right):
				if(left_rec.t < right_rec.t):
					rec = left_rec
				else:
					rec = right_rec
				return (True,rec)
			elif(hit_left):
				return (True,left_rec)
			elif(hit_right):
				return (True,right_rec)
			else:
				return(False,rec)
		else:
			return (False,rec)

####
'''
hitable containers
'''
####

'''
flip normal hitable
'''
class flip_normals(hitable):
	def __init__(self,p: hitable):
		self.p = p 
	def hit(self,r:ray, t_min:float, t_max: float):
		is_hit,rec = self.p.hit(r,t_min,t_max)
		if is_hit:
			rec.normal = -rec.normal
			return(True, rec)
		else:
			return (False,rec)
	def bounding_box(self, t0: float, t1: float):
		return self.p.bounding_box(t0,t1)

class translate(hitable):
	def __init__(self,p: hitable,offset: vec3):
		self.offset = offset
		self.p = p 
	def hit(self,r:ray, t_min:float, t_max: float):
		moved_r = ray(r.origin - self.offset,r.direction,r.time)
		#print(self.p)
		is_hit,rec = self.p.hit(moved_r,t_min,t_max)
		if is_hit:
			rec.p += self.offset
			return (True,rec)
		else:
			return (False,rec)
	def bounding_box(t0: float, t1: float):
		box = None
		found_box,box = self.p.bounding_box(t0,t1)
		if found_box:
			box = aabb(box._min + self.offset, box._max + self.offset)
			return (True,box)
		else: 
			return (False,box)

class rotate_y(hitable):
	def __init__(self,p: hitable, angle: float):  
		self.radians = (pi / 180.0) * angle;
		self.sin_theta = sin(self.radians)
		self.cos_theta = cos(self.radians)
		self.p = p
		self.hasbox,self.bbox = self.p.bounding_box(0, 1)
		self._min_ = vec3(FLT_MAX, FLT_MAX, FLT_MAX)
		self._max_ = vec3(-FLT_MAX, -FLT_MAX, -FLT_MAX)
		for i in range(2):
			for j in range(2):
				for k in range(2):
					x = i*self.bbox._max[0] + (1-i)*self.bbox._min[0]
					y = j*self.bbox._max[1] + (1-j)*self.bbox._min[1]
					z = k*self.bbox._max[2] + (1-k)*self.bbox._min[2]
					newx = self.cos_theta*x + self.sin_theta*z;
					newz = -self.sin_theta*x + self.cos_theta*z;
					tester = vec3(newx, y, newz);
					for c in range(3):
						if ( tester[c] > self._max_[c] ):
							self._max_[c] = tester[c]
						if ( tester[c] < self._min_[c] ):
							self._min_[c] = tester[c]
		self.bbox = aabb(self._min_, self._max_)
	def hit(self,r:ray, t_min:float, t_max: float):
		new_origin_x = self.cos_theta*r.origin[0] - self.sin_theta*r.origin[2]
		# this ensures that new_origin_y populates a new value with no reference to origin r.origin[1]
		# this ensures that original ray data is not polluted when we stick it into new ray
		# we do this instead copy or deepcopy because both of those commands are incredibly expensive
		# and we only care about affecting numerical primitives here, honestly python needs a better way to do this...
		new_origin_y = 1.0 * r.origin[1]
		new_origin_z = self.sin_theta*r.origin[0] + self.cos_theta*r.origin[2]
		new_direction_x  = self.cos_theta*r.direction[0] - self.sin_theta*r.direction[2]
		new_direction_y = 1.0 * r.direction[1]
		new_direction_z = self.sin_theta*r.direction[0] + self.cos_theta*r.direction[2];
		new_time = r.time * 1.0

		rotated_r = ray(vec3(new_origin_x,new_origin_y,new_origin_z),
						vec3(new_direction_x,new_direction_y,new_direction_z),
						new_time) 
		is_hit,rec = self.p.hit(rotated_r, t_min, t_max)
		if (is_hit):
			p_x = self.cos_theta*rec.p[0] + self.sin_theta*rec.p[2];
			p_z = -self.sin_theta*rec.p[0] + self.cos_theta*rec.p[2];
			normal_x = self.cos_theta*rec.normal[0] + self.sin_theta*rec.normal[2];
			normal_z = -self.sin_theta*rec.normal[0] + self.cos_theta*rec.normal[2];
			rec.p[0],rec.p[2] =p_x,p_z;
			rec.normal[0],rec.normal[2] = normal_x,normal_z;
			return (True,rec);
		else: 
			return (False,rec);
		def bounding_box(self,t0: float, t1: float):
			return (self.hasbox,self.bbox)





