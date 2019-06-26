import sys
sys.path.append("./src/core/")
from  ray import * 
from utils import *
from hitable import * 
from geometry import * 
import numpy as np
import matplotlib.pyplot as plt

MAX_FLOAT = sys.float_info.max

# def hit_sphere(center: np.ndarray ,radius: float,r: ray):
# 	oc = r.origin() - center

# 	a = tiledot(r.direction(),r.direction())
# 	b = 2.0 * tiledot(oc,r.direction())
# 	c =  tiledot(oc,oc) - radius ** 2
# 	discriminant = b ** 2 - 4 * a * c 
# 	return np.where((discriminant > 0),(0 - b - np.sqrt(discriminant))/ (a * 2.0),-1.0)

def color(r: ray,world: list,tile_shape):
	t = 0
	tile_x,tile_y = tile_shape
	hit_color = tile(np.zeros((tile_x,tile_y,3)))
	hit_anything,rec_list = iterate_hit_list(r,tile(np.ones((nx,ny)) * 0.001),
							tile(np.ones((nx,ny)) * MAX_FLOAT),world)
	#print(len(rec_list))
	for record in rec_list:
		N = record.normal
		mask = ~np.all(record.t == -1.0, axis=-1)
		t += tile(mask) * record.t
		hit_color += tile(mask) * vec3(N[:,:,0] + 1,N[:,:,1] + 1,N[:,:,2] + 1) * 0.5

	
	unit_direction = unit_vector(r.direction())
	t2 = tile(0.5 * (unit_direction[:,:,1] + 1.0))
	sky_color = vec3(1.0,1.0,1.0) * (1.0 - t2) + vec3(0.5,0.7,1.0) * t2
	return np.where(t > 0.0, hit_color,sky_color)

def main(nx: float = 200, ny: float = 100):
	j = np.tile(np.arange(0,ny,1),reps=(nx,1))
	i = np.tile(np.arange(0,nx,1),reps=(ny,1)).T

	lower_left_corner = vec3(-2.0,-1.0,-1.0)
	horizontal = vec3(4.0,0,0)
	vertical = vec3(0.0,2,0)
	origin = vec3(0.0,0.0,0.0)
	hit_object_list = []
	hit_object_list.append(sphere(vec3(0,0,-1),0.5))
	hit_object_list.append(sphere(vec3(0,-100.5,-1),100))

	# print(i.shape)
	# print(j)
	u = tile(i/nx)
	v = tile(j/ny)

	r = ray(origin,lower_left_corner + u * horizontal + v * vertical)
	#print(len(hit_object_list))
	col = color(r,hit_object_list,output_shape=(nx,ny))

	#print(unit_vector(vec3(1,2,3)).shape)

	#b = np.ones_like(r) * 0.2 

	#colors will be assumed to be (..,3)
	# this assumes that all functions will operate on 3-vectors
	#col = np.dstack((r,g,b))
	#print(col.shape)
	#unit_vector(col)
	ir = 255.99 * col[:,:,0]
	ig = 255.99 * col[:,:,1]
	ib = 255.99 * col[:,:,2]
	output = np.dstack((ir,ig,ib))
	# print(output.shape)
	plt.imsave("output.png",np.rot90(output.astype(int)))
if __name__ == "__main__": 
	main()
