from geometry import * 
from math import *
import random

def random_in_unit_disk():
	p = vec3(1.0,1.0,1.0)
	while p.dot(p) >= 1.0:
		p = 2.0 * vec3(random.random(),random.random(),0) - vec3(1,1,0)
	return p
class camera:
	def __init__(self,lookfrom: vec3,lookat: vec3, vup: vec3,
					  vfov: float,aspect: float, aperture: float, focus_dist: float,t0: float,t1: float):

		

		self.time0 = t0
		self.time1 = t1
		self.lens_radius = aperture / 2
		self.theta = vfov * pi/180
		self.half_height = tan(self.theta/2)
		self.half_width = aspect * self.half_height
		self.origin = lookfrom
		self.focus_dist = focus_dist
		self.aperture = aperture
		self.w = unit_vector(lookfrom - lookat)
		self.u = unit_vector(vup.cross(self.w))
		self.v = self.w.cross(self.u)
		self.lower_left_corner = self.origin - self.half_width * self.focus_dist * self.u - self.half_height * self.focus_dist * self.v - self.focus_dist * self.w

		self.horizontal = 2 * self.half_width * self.focus_dist * self.u 
		self.vertical = 2 * self.half_height * self.focus_dist * self.v
	def get_ray(self,s: float,t: float):
		rd = self.lens_radius * random_in_unit_disk()
		offset = self.u * rd.x() + self.v * rd.y()
		time = self.time0 + random.random() * (self.time1-self.time0)
		return ray(self.origin + offset,self.lower_left_corner + s * self.horizontal + t * self.vertical - self.origin - offset,time)
