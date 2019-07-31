import sys
from math import * 
from hitable import * 
from geometry import *
from texture import * 
from abc import ABC,abstractmethod
import random


'''
reflectivity polynomial approximation
by Christophe Schlick
'''

def schlick(cosine: float, ref_idx: float):
	r0 = (1 - ref_idx) / (1 + ref_idx)
	r0 = r0 * r0
	return r0 + (1-r0) * pow((1-cosine),5)

'''
reflection about normal
'''
def reflect(incoming_vector: vec3, normal: vec3):
	outgoing_vector = incoming_vector - 2 * incoming_vector.dot(normal) * normal;
	return outgoing_vector

'''
randomly sample a direction on the unit sphere
'''
def random_unit_sphere():
    p = vec3(1,1,1)
    while p.squared_length() >= 1.0:
        p = 2.0 * vec3(random.random(),random.random(),random.random()) - vec3(1.0,1.0,1.0)
    return p 

'''
refract and return refracted vector
'''
def refract(incoming_vector: vec3, normal: vec3, ni_over_nt: float):
	uv = unit_vector(incoming_vector)
	dt = uv.dot(normal)
	refracted = vec3(0,0,0)
	discriminant = 1.0 - ni_over_nt * ni_over_nt * (1-dt*dt)
	if(discriminant > 0):
		refracted = ni_over_nt * (uv - normal * dt) - normal * sqrt(discriminant)
		return True,refracted
	else:
		return False, refracted


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
	'''
	base function so non-emissive materials don't emit anything
	'''
	def emitted(self,u: float, v: float, p: vec3):
		return vec3(0,0,0)


class lambertian(material):
	def __init__(self,albedo: texture):
		self.albedo = albedo
	def scatter(self,r_in: ray, rec):
		target = rec.p + rec.normal + random_unit_sphere()
		scattered = ray(rec.p,target - rec.p,r_in.time)
		attenuation = self.albedo.value(rec.u,rec.v,rec.p)
		return True,(scattered,attenuation)

class metal(material):
	def __init__(self,albedo: vec3,f: float = 0.0):
		if f < 1.0:
			self.fuzz = f
		else:
			self.fuzz = 1.0
		self.albedo = albedo
	def scatter(self,r_in: ray, rec):
		reflected = reflect(unit_vector(r_in.direction),rec.normal)
		scattered = ray(rec.p,reflected + self.fuzz * random_unit_sphere(),r_in.time)
		attenuation = self.albedo
		return scattered.direction.dot(rec.normal) > 0,(scattered,attenuation)

class dielectric(material):
	def __init__(self,ri: float):
		self.ref_idx = ri
	def scatter(self,r_in: ray, rec):
		outward_normal = None
		ni_over_nt = None
		refracted = None;
		scattered = None;
		reflected = reflect(r_in.direction,rec.normal)
		attenuation = vec3(1.0,1.0,1.0)
		reflect_prob = None
		cosine = None

		if(r_in.direction.dot(rec.normal) > 0):
			outward_normal = -rec.normal
			ni_over_nt = self.ref_idx
			cosine = self.ref_idx * r_in.direction.dot(rec.normal) / r_in.direction.length()
		else:
			outward_normal = rec.normal
			ni_over_nt = 1.0/self.ref_idx
			cosine = -r_in.direction.dot(rec.normal) / r_in.direction.length()

		if_refract,refracted = refract(r_in.direction,outward_normal,ni_over_nt)
		if if_refract:
			reflect_prob = schlick(cosine,self.ref_idx)
			#scattered = ray(rec.p,refracted)
		else:
			scattered = ray(rec.p,reflected,r_in.time)
			reflect_prob = 1.0
			#return False, (scattered,attenuation)
		if random.random() < reflect_prob:
			scattered = ray(rec.p,reflected,r_in.time)
		else: 
			scattered = ray(rec.p,refracted,r_in.time)

		return True,(scattered,attenuation)

'''

light material 

'''
class diffuse_light(material): 
	def __init__(self,tex: texture):
		self.emit = tex

	def scatter(self,r_in: ray, rec):
		'''
		diffuse light do not reflect, simply emit
		'''
		return False,(0,0)
	def emitted(self,u: float, v: float, p: vec3 ):
		'''
		return color associated w/ texture

		'''
		return self.emit.value(u,v,p)


'''

isotropic function

'''

class isotropic(material):
	def __init__(self,a: texture):
		self.albedo = a 
	def scatter(self,r_in: ray, rec):
		scattered = ray(rec.p,random_unit_sphere(),r_in.time)
		attenuation = self.albedo.value(rec.u,rec.v,rec.p)
		return True,(scattered,attenuation)








