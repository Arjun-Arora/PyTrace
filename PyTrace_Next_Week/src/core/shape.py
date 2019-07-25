import sys
from hitable import * 
import math
from geometry import *

def get_sphere_uv(p: vec3):
	phi = atan2(p[2],p[0])
	theta = asin(p[1])
	u = 1 - (phi + pi)/ (2 * pi )
	v = (theta + pi / 2) / ( pi )
	return u,v

class sphere(hitable):
	def __init__(self,center: vec3,radius: float,mat: material):
		self.center = center
		self.radius = radius
		self.mat = mat
	def hit(self,r: ray , t_min: float,t_max: float):
		rec = hit_record()
		rec.mat = self.mat
		oc = r.origin - self.center
		a = (r.direction).dot(r.direction)
		b = oc.dot(r.direction)
		c = oc.dot(oc) - (self.radius * self.radius)
		discriminant = b * b - (a * c)
		if (discriminant > 0 ): 
			temp = (-b - math.sqrt(b * b - a * c))/a
			if ((temp < t_max and temp > t_min)):
				#print('hit this')
				rec.t = temp
				rec.p = r(rec.t)
				rec.u,rec.v = get_sphere_uv((rec.p-self.center)/self.radius)
				rec.normal = (rec.p - self.center)/self.radius
				return (True, rec)
			temp = (-b + math.sqrt(b * b - a * c))/a
			if ((temp < t_max and temp > t_min)):
				#print('hit this')
				rec.t = temp
				rec.p = r(rec.t)
				rec.u,rec.v = get_sphere_uv((rec.p-self.center)/self.radius)
				rec.normal = (rec.p - self.center)/self.radius
				return (True, rec)
		# print('got here with discriminant: {}'.format(discriminant))
		return (False,rec)
	def bounding_box(self, t0: float=None, t1: float=None):
		box = aabb(self.center - vec3(self.radius,self.radius,self.radius),
				  center + vec3(self.radius,self.radius,self.radius))
		return (True,box);




class moving_sphere(hitable):
	def __init__(self,cen0: vec3, cen1: vec3, t0: float, t1: float, r: float, mat: material):
		self.center0 = cen0
		self.center1 = cen1
		self.time0 = t0
		self.time1 = t1
		self.radius = r 
		self.mat = mat
	def curr_center(self,time: float):
		return self.center0 + ((time - self.time0)/(self.time1-self.time0)) * (self.center1 - self.center0)

	def hit(self,r: ray , t_min: float,t_max: float):
		rec = hit_record()
		rec.mat = self.mat
		#oc = r.origin - self.center
		oc = r.origin - self.curr_center(r.time)
		a = (r.direction).dot(r.direction)
		b = oc.dot(r.direction)
		c = oc.dot(oc) - (self.radius * self.radius)
		discriminant = b * b - (a * c)
		if (discriminant > 0 ): 
			temp = (-b - math.sqrt(b * b - a * c))/a
			if ((temp < t_max and temp > t_min)):
				rec.t = temp
				rec.p = r(rec.t)
				#rec.normal = (rec.p - self.center)/self.radius
				rec.normal = (rec.p - self.curr_center(r.time))/self.radius
				return (True, rec)
			temp = (-b + math.sqrt(b * b - a * c))/a
			if ((temp < t_max and temp > t_min)):
				#print('hit this')
				rec.t = temp
				rec.p = r(rec.t)
				#rec.normal = (rec.p - self.center)/self.radius
				rec.normal = (rec.p - self.curr_center(r.time))/self.radius
				return (True, rec)
		return (False,rec)
	def bounding_box(self, t0: float, t1: float):
		box = sorrounding_box(sphere(self.curr_center(t0),self.radius,self.mat).bounding_box()[1],
			  				  sphere(self.curr_center(t1),self.radius,self.mat).bounding_box()[1])
		return (True,box)


'''
x-y axis aligned rectangle
'''
class xy_rect(hitable):
	def __init__(self,x0: float, x1: float, y0: float, y1: float, k: float, mat: material):
		self.x0 = x0
		self.x1 = x1
		self.y0 = y0
		self.y1 = y1
		self.k = k 
		self.mat = mat 
	def hit(self,r: ray , t0: float,t1: float):
		rec = hit_record()
		rec.mat = self.mat
		t = (self.k - r.origin[2]) / r.direction[2]
		if t < t0 or t > t1:
			return (False,rec)
		x = r.origin[0] + t * r.direction[0]
		y = r.origin[1] + t * r.direction[1]
		if x < self.x0 or x > self.x1 or y < self.y0 or y > self.y1: 
			return (False,rec)
		rec.u = (x-self.x0)/(self.x1-self.x0)
		rec.v = (y-self.y0)/(self.y1-self.y0)
		rec.t = t 
		rec.p = r(rec.t)
		rec.normal = vec3(0,0,1)
		return (True,rec)
	def bounding_box(self,t0: float, t1: float ): 
		box = aabb(vec3(self.x0,self.y0,self.k-0.0001),vec3(self.x1,self.y1,self.k + 0.0001))
		return (True,box)

'''
x-z axis aligned rectangle
'''
class xz_rect(hitable):
	def __init__(self,x0: float, x1: float, z0: float, z1: float, k: float, mat: material):
		self.x0 = x0
		self.x1 = x1
		self.z0 = z0
		self.z1 = z1
		self.k = k 
		self.mat = mat 
	def hit(self,r: ray , t0: float,t1: float):
		rec = hit_record()
		rec.mat = self.mat
		t = (self.k - r.origin[1]) / r.direction[1]
		if t < t0 or t > t1:
			return (False,rec)
		x = r.origin[0] + t * r.direction[0]
		z = r.origin[2] + t * r.direction[2]
		if x < self.x0 or x > self.x1 or z < self.z0 or z > self.z1: 
			return (False,rec)
		rec.u = (x-self.x0)/(self.x1-self.x0)
		rec.v = (z-self.z0)/(self.z1-self.z0)
		rec.t = t 
		rec.p = r(rec.t)
		rec.normal = vec3(0,1,0)
		return (True,rec)
	def bounding_box(self,t0: float, t1: float ): 
		box = aabb(vec3(self.x0,self.k-0.0001,self.z0),vec3(self.x1,self.k + 0.0001,self.z1))
		return (True,box)


'''
y-z axis aligned rectangle
'''
class yz_rect(hitable):
	def __init__(self,y0: float, y1: float, z0: float, z1: float, k: float, mat: material):
		self.y0 = y0
		self.y1 = y1
		self.z0 = z0
		self.z1 = z1
		self.k = k 
		self.mat = mat 
	def hit(self,r: ray , t0: float,t1: float):
		rec = hit_record()
		rec.mat = self.mat
		t = (self.k - r.origin[0]) / r.direction[0]
		if t < t0 or t > t1:
			return (False,rec)
		y = r.origin[1] + t * r.direction[1]
		z = r.origin[2] + t * r.direction[2]
		if y < self.y0 or y > self.y1 or z < self.z0 or z > self.z1: 
			return (False,rec)
		rec.u = (y-self.y0)/(self.y1-self.y0)
		rec.v = (z-self.z0)/(self.z1-self.z0)
		rec.t = t 
		rec.p = r(rec.t)
		rec.normal = vec3(1,0,0)
		return (True,rec)
	def bounding_box(self,t0: float, t1: float ): 
		box = aabb(vec3(self.k-0.0001,self.y0,self.z0),vec3(self.k + 0.0001,self.y1,self.z1))
		return (True,box)