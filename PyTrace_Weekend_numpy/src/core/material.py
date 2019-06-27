from abc import ABC,abstractmethod
from utils import * 
from ray import * 
from hitable import * 
import numpy as np 

class material(ABC):
	def __init__(self):
		pass
	def __scatter__(self,r: ray,rec):
		pass

def reflect(incoming_vector, normal):
	outgoing_vector = tile(incoming_vector) - 2 * \
					  tile(tiledot(incoming_vector,normal)) * normal;
	return outgoing_vector


def random_in_unit_sphere(arr: np.ndarray):
	shape = arr.shape
	random_tile_in_sphere = np.random.randn(*shape)
	# print(random_tile_in_sphere.shape)
	# print(np.linalg.norm(random_tile_in_sphere,axis=2).shape)
	random_tile_in_sphere /= tile(np.linalg.norm(random_tile_in_sphere,axis=2))
	return  random_tile_in_sphere

class lambertian(material):
	def __init__(self,albedo: vec3):
		self.albedo = albedo
	def scatter(self,r_in: ray, rec):
		target = rec.p + rec.normal + random_in_unit_sphere(rec.normal)
		#mask = ~np.all(rec.t == -1.0, axis=-1)
		scattered = ray(rec.p,target - rec.p)
		attenuation = self.albedo
		return True,(scattered,attenuation)

class metal(material):
	def __init__(self,albedo: vec3,f: float = 0.0):
		if f < 1.0:
			self.fuzz = f
		else:
			self.fuzz = 1.0
		self.albedo = albedo
	def scatter(self,r_in: ray, rec):
		reflected = reflect(unit_vector(r_in.direction()),rec.normal)
		scattered = ray(rec.p,reflected + self.fuzz * random_in_unit_sphere(reflected))
		attenuation = self.albedo
		return np.any(tiledot(scattered.direction(),rec.normal) > 0),(scattered,attenuation)