import numpy as np
from abc import ABC,abstractmethod
from utils import * 
from ray import * 
from hitable import * 
import sys
MAX_FLOAT = sys.float_info.max

class sphere(hitable):
	def __init__(self,center: np.ndarray, radius: float,mat):
		'''
		center: vec3 center of sphere
		radius: float radius of sphere
		ray: 
		'''
		self.center = center
		self.radius = radius
		self.mat = mat
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
		square = np.sqrt(np.maximum(0,discriminant))
		dist_to_hit = (-b - square) / 2
		dist_to_hit_2 = (-b + square) / 2

		distance = np.where( (dist_to_hit > 0) & (dist_to_hit < dist_to_hit_2), dist_to_hit,dist_to_hit_2)
		hit = (discriminant > 0) & (distance > 0)

		t = tile(np.where(hit,distance,-1.0))
		p = r(t)
		normal =((p - self.center)/self.radius)
		rec = hit_record(t,p,normal,self.mat)
		#print(np.any(rec.t > 0))
		return np.any(rec.t > 0),rec 