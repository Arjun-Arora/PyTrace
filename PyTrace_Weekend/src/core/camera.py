from geometry import * 
from math import *
import random

def random_in_unit_disk():
	p = vec3((1,1,1))
	while p.dot(p) >= 1.0:
		p = (vec3((random.random(),random.random(),0)) - vec3((1,1,0))) * 2.0
	return p
class camera:
	def __init__(self,lookfrom: vec3,lookat: vec3, vup: vec3,
					  vfov: float,aspect: float, aperture: float, focus_dist: float):

		self.lens_radius = aperture / 2
		# u = None
		# v = None
		# w = None
		self.theta = vfov * pi/180
		self.half_height = tan(self.theta/2)
		self.half_width = aspect * self.half_height
		self.origin = lookfrom
		self.focus_dist = focus_dist
		self.aperture = aperture
		self.w = unit_vector(lookfrom - lookat)
		self.u = unit_vector(vup.cross(self.w))
		self.v = self.w.cross(self.u)

		part0 = self.origin - self.half_width
		part1 = self.u * self.focus_dist
		self.lower_left_corner = part0 * part1  - self.v * self.half_height * self.focus_dist - self.w * self.focus_dist

		self.horizontal = self.u * 2 * self.half_width * self.focus_dist
		self.vertical = self.v * 2 * self.half_height * self.focus_dist
	def get_ray(self,s: float,t: float):
		rd = random_in_unit_disk() * self.lens_radius
		offset = self.u * rd.x() + self.v * rd.y()
		return ray(self.origin + offset,
				   self.lower_left_corner + self.horizontal * s + self.vertical * t- self.origin - offset)
