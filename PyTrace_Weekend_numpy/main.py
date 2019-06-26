import sys
sys.path.append("./src/core/")
from  ray import * 
from utils import *
import numpy as np
import matplotlib.pyplot as plt


def hit_sphere(center: np.ndarray ,radius: float,r: ray):
	oc = r.origin() - center

	a = tiledot(r.direction(),r.direction())
	b = 2.0 * tiledot(oc,r.direction())
	c =  tiledot(oc,oc) - radius ** 2
	discriminant = b ** 2 - 4 * a * c 
	return np.where((discriminant > 0),(0 - b - np.sqrt(discriminant))/ (a * 2.0),-1.0)

def color(r: ray):
	#print(r.direction)
	t = tile(hit_sphere(vec3(0,0,-1),0.5,r))
	N = unit_vector((r(t) - vec3(0, 0, -1)))

	#print(N + 1)

	hit_color = vec3(N[:,:,0] + 1,N[:,:,1] + 1,N[:,:,2] + 1) * 0.5
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

	# print(i.shape)
	# print(j)
	u = tile(i/nx)
	v = tile(j/ny)

	r = ray(origin,lower_left_corner + u * horizontal + v * vertical)
	col = color(r)

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
