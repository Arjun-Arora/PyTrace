import sys
sys.path.append("./src/core/")
from  ray import * 
from utils import *
from hitable import * 
from geometry import *
from camera import *  
from material import * 
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from mpl_toolkits.mplot3d import Axes3D

MAX_FLOAT = sys.float_info.max


def color(r: ray,world: list,tile_shape,depth = 0,max_depth = 2):
	t = 0
	target = 0
	tile_x,tile_y = tile_shape
	hit_color = tile(np.zeros((tile_x,tile_y,3)))
	hit_anything,rec_list,closest_hit = iterate_hit_list(r,tile(np.ones((tile_x,tile_y)) * 1e-9),
										tile(np.ones((tile_x,tile_y)) * MAX_FLOAT),world)
	if hit_anything and depth <= max_depth:
		for rec in rec_list:
			scattered = None
			attenuation = None
			if_scatter,(scattered,attenuation) = rec.mat.scatter(r,rec)
			if if_scatter:
			#masks out all values that we didn't get hits for 
				mask = ~np.all(rec.t == -1.0, axis=-1)
				t += tile(mask) * (closest_hit == rec.t) *  rec.t
				#target = rec.p + rec.normal + tile(mask) * random_in_unit_sphere(rec.normal.shape)
				#mask out all color contributions that are calculated incorrectly using a mask
				hit_color += 0.5 * tile(mask) * (closest_hit == rec.t) * attenuation *  color(scattered,world,tile_shape,depth+1,max_depth)


	# if hit_anything and depth <= max_depth:
	# 	for rec in rec_list:
	# 		mask =  tile(~np.all(rec.t == -1.0, axis=-1))  & (closest_hit == rec.t)
	# 		t += mask * rec.t
	# 		#bug cannot be in random because incorrect coloring appears without random
	# 		target = rec.p + rec.normal + random_in_unit_sphere(rec.normal)
	# 		hit_color += mask * 0.5 * color(ray(rec.p, target - rec.p),world,tile_shape,depth+1,max_depth)

	# for record in rec_list:
	# 	N = record.normal
	# 	mask = ~np.all(record.t == -1.0, axis=-1)
	# 	t += tile(mask) *  (closest_hit == record.t) * record.t
	# 	hit_color += tile(mask) * (closest_hit == record.t) * vec3(N[:,:,0] + 1,N[:,:,1] + 1,N[:,:,2] + 1) * 0.5

	
	unit_direction = unit_vector(r.direction())
	#print((unit_direction ** 2).sum(axis=-1) ** 0.5)
	t2 = tile(0.5 * (unit_direction[:,:,1] + 1.0))

	sky_color = vec3(1.0,1.0,1.0) * (1.0 - t2) + vec3(0.5,0.7,1.0) * t2

	return np.where(t > 0, hit_color,sky_color)

def main(nx: float = 200, ny: float = 100,ns: float = 100):
	j = np.tile(np.arange(0,ny,1),reps=(nx,1))
	i = np.tile(np.arange(0,nx,1),reps=(ny,1)).T

	hit_object_list = []
	hit_object_list.append(sphere(vec3(0,0,-1),0.5,lambertian(vec3(0.8,0.3,0.3))))
	hit_object_list.append(sphere(vec3(0,-100.5,-1),100,lambertian(vec3(0.8,0.8,0.0))))	
	hit_object_list.append(sphere(vec3(1,0,-1),0.5,metal(vec3(0.8,0.6,0.2),1.0)))
	hit_object_list.append(sphere(vec3(-1,0,-1),0.5,metal(vec3(0.8,0.8,0.8),0.3)))



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
	ir = 255.99 * np.sqrt(col[:,:,0])
	ig = 255.99 * np.sqrt(col[:,:,1])
	ib = 255.99 * np.sqrt(col[:,:,2])
	output = np.dstack((ir,ig,ib))
	# print(output.shape)
	plt.imsave("output.png",np.rot90(output.astype(int)))
if __name__ == "__main__": 
	main(200,100,100)
	# X = random_in_unit_sphere(np.random.randn(200,100,3))
	# fig = plt.figure()
	# ax = fig.add_subplot(111)
	# ax.scatter(X[:,:,0],X[:,:,1],X[:,:,2])
	# plt.show()
