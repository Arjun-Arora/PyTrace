import sys
from hitable import * 
import math
from geometry import *
class sphere(hitable):
	def __init__(self,
				 center,radius):
		self.center = center
		self.radius = radius
	def hit(self,r: ray , t_min: float,t_max: float):
		rec = hit_record()
		oc = r.origin() - self.center
		a = (r.direction()).dot(r.direction())
		b = 2.0 * oc.dot(r.direction())
		c = oc.dot(oc) - self.radius * self.radius
		discriminant = b * b - 4 * a * c
		if (discriminant > 0 ): 
			temp = (-b - math.sqrt(b * b - a * c))
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
