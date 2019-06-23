import sys
from math import * 
from hitable import * 
from geometry import *
from abc import ABC,abstractmethod
import random

'''
reflection about normal
'''
def reflect(incoming_vector: vec3, normal: vec3):
	outgoing_vector = incoming_vector - 2 * incoming_vector.dot(normal) * normal;
	return outgoing_vector
'''
randomly sample a direction on the unit circle
'''
def random_unit_sphere():
    p = vec3(1,1,1)
    while p.squared_length() >= 1.0:
        p = 2.0 * vec3(random.random(),random.random(),random.random()) - vec3(1.0,1.0,1.0)
    return p 
'''
abstract material
'''
class material(ABC):
	def __init__(self):
		pass
	'''
	returns whether we scatter, along with scattered spectra and attentuated spectra
	'''
	def scatter(r: ray, rec):
		pass

class lambertian(material):
	def __init__(self,albedo: vec3):
		self.albedo = albedo
	def scatter(self,r_in: ray, rec):
		target = rec.p + rec.normal + random_unit_sphere()
		scattered = ray(rec.p,target - rec.p)
		attenuation = self.albedo
		return True,(scattered,attenuation)

class metal(material):
	def __init__(self,albedo: vec3):
		self.albedo = albedo
	def scatter(self,r_in: ray, rec):
		reflected = reflect(unit_vector(r_in.direction()),rec.normal)
		scattered = ray(rec.p,reflected)
		attenuation = self.albedo
		return scattered.direction().dot(rec.normal) > 0,(scattered,attenuation)




