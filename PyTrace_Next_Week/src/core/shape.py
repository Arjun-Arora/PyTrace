import sys
from hitable import * 
import math
from geometry import *
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
				rec.normal = (rec.p - self.center)/self.radius
				return (True, rec)
			temp = (-b + math.sqrt(b * b - a * c))/a
			if ((temp < t_max and temp > t_min)):
				#print('hit this')
				rec.t = temp
				rec.p = r(rec.t)
				rec.normal = (rec.p - self.center)/self.radius
				return (True, rec)
		# print('got here with discriminant: {}'.format(discriminant))
		return (False,rec)
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