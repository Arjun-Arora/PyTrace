import sys
sys.path.append("./src/core/")
from  ray import * 
from utils import *
from hitable import * 
from geometry import *
from camera import *  
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from mpl_toolkits.mplot3d import Axes3D

MAX_FLOAT = sys.float_info.max

def random_in_unit_sphere(arr: np.ndarray):
	shape = arr.shape
	random_tile_in_sphere = np.random.randn(*shape)
	# print(random_tile_in_sphere.shape)
	# print(np.linalg.norm(random_tile_in_sphere,axis=2).shape)
	random_tile_in_sphere /= tile(np.linalg.norm(random_tile_in_sphere,axis=2))
	return  random_tile_in_sphere
	

def color(r: ray,world: list,tile_shape,depth = 0,max_depth = 4):
	t = 0
	target = 0
	tile_x,tile_y = tile_shape
	hit_color = tile(np.zeros((tile_x,tile_y,3)))
	hit_anything,rec_list = iterate_hit_list(r,tile(np.ones((tile_x,tile_y)) * 0.01),
							tile(np.ones((tile_x,tile_y)) * MAX_FLOAT),world)
	if hit_anything and depth <= max_depth:
		for rec in rec_list:
			#masks out all values that we didn't get hits for 
			mask = ~np.all(rec.t == -1.0, axis=-1)
			t += tile(mask) * rec.t
			target = rec.p + rec.normal + tile(mask) * random_in_unit_sphere(rec.normal)
			#mask out all color contributions that are calculated incorrectly using a mask
			hit_color += 0.5 * tile(mask)  * color(ray(rec.p,  target-rec.p),world,tile_shape,depth+1,max_depth)

	# for record in rec_list:
	# 	N = record.normal
	# 	mask = ~np.all(record.t == -1.0, axis=-1)
	# 	t += tile(mask) * record.t
	# 	hit_color += tile(mask) * vec3(N[:,:,0] + 1,N[:,:,1] + 1,N[:,:,2] + 1) * 0.5

	
	unit_direction = unit_vector(r.direction())
	t2 = tile(0.5 * (unit_direction[:,:,1] + 1.0))
	sky_color = vec3(1.0,1.0,1.0) * (1.0 - t2) + vec3(0.5,0.7,1.0) * t2
	return np.where(t > 0.0, hit_color,sky_color)

def main(nx: float = 200, ny: float = 100,ns: float = 100):
	j = np.tile(np.arange(0,ny,1),reps=(nx,1))
	i = np.tile(np.arange(0,nx,1),reps=(ny,1)).T

	hit_object_list = []
	hit_object_list.append(sphere(vec3(0,0,-1),0.5))
	hit_object_list.append(sphere(vec3(0,-100.5,-1),100))
	col = np.zeros((nx,ny,3))
	cam = camera()
	with tqdm(total=ns) as pbar:
		for s in range(0,ns):
			u = tile((i + np.random.rand(nx,ny))/nx)
			v = tile((j + np.random.rand(nx,ny))/ny) 

			r = cam.get_ray(u,v)
			col += color(r,hit_object_list,tile_shape=(nx,ny))
			pbar.update(1)

	col /= float(ns)
	ir = 255.99 * col[:,:,0]
	ig = 255.99 * col[:,:,1]
	ib = 255.99 * col[:,:,2]
	output = np.dstack((ir,ig,ib))
	# print(output.shape)
	plt.imsave("output_2.png",np.rot90(output.astype(int)))
if __name__ == "__main__": 
	main(200,100,10)
	# X = random_in_unit_sphere(np.random.randn(200,100,3))
	# fig = plt.figure()
	# ax = fig.add_subplot(111)
	# ax.scatter(X[:,:,0],X[:,:,1],X[:,:,2])
	# plt.show()
