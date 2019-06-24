from geometry import * 
from math import *

class camera:
	def __init__(self,lookfrom: vec3,lookat: vec3, vup: vec3, vfov: float,aspect: float):
		u = None
		v = None
		w = None
		self.theta = vfov * pi/180
		self.half_height = tan(self.theta/2)
		self.half_width = aspect * self.half_height
		self.origin = lookfrom
		w = unit_vector(lookfrom - lookat)
		u = unit_vector(vup.cross(w))
		v = w.cross(u)


		self.lower_left_corner = vec3(-self.half_width,-self.half_height,-1.0)
		self.lower_left_corner = self.origin - self.half_width * u -self.half_height * v - w;

		self.horizontal = 2 * self.half_width * u 
		self.vertical = 2 * self.half_height * v
	def get_ray(self,u: float,v: float):
		return ray(self.origin,self.lower_left_corner + u * self.horizontal + v * self.vertical - self.origin)
