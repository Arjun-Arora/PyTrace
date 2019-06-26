import numpy as np
from abc import ABC,abstractmethod
from utils import * 
from ray import * 
from hitable import * 
import sys
MAX_FLOAT = sys.float_info.max

class sphere(hitable):
	def __init__(self,center: np.ndarray, radius: float):
		'''
		center: vec3 center of sphere
		radius: float radius of sphere
		ray: 
		'''
		self.center = center
		self.radius = radius
	def hit(self,r: ray,t_min: np.ndarray,t_max: np.ndarray):
		'''
		t_min: tile of minimum values along rays to hit (m x n x 1)
		t_min: tile of max values along rays to hit (m x n x 1)
		r: ray tile
		
		returns: if any of the rays in tile hit, and the hit records of all tiles 
		'''
		oc = r.origin() - self.center
		a = tile(tiledot(r.direction(),r.direction()))
		b = tile(2.0 * tiledot(oc,r.direction()))
		c =  tile(tiledot(oc,oc) - self.radius ** 2)
		discriminant = tile(b ** 2 - 4 * a * c )
		dist_to_hit = tile((0 - b - np.sqrt(discriminant)))
		# print(t_min.shape)
		# print(t_max.shape)
		# print((dist_to_hit > t_min).shape)
		# print(discriminant.shape)
		# print(dist_to_hit.shape)
		# print(dist_to_hit < t_max)
		t = tile(np.where((discriminant > 0) * (dist_to_hit > t_min) * (dist_to_hit < t_max),
						  dist_to_hit/(a * 2.0),-1.0))
		p = r(t)
		normal = np.where( p != r(-1.0),(p - self.center)/self.radius,0)
		rec = hit_record(t,p,normal)
		#print(np.any(rec.t > 0))
		return np.any(rec.t > 0),rec 