import sys
sys.path.append("./src/core/")
from  ray import * 
from utils import *
import numpy as np
import matplotlib.pyplot as plt

def color(r: ray):
	#print(r.direction)
	unit_direction = unit_vector(r.direction())
	t = coordinatize(0.5 * (unit_direction[:,:,1]) + 1.0)
	return (1.0-t) * vectorize(np.array((1.0,1.0,1.0))) + t * vectorize(np.array((0.5,0.7,1.0)))

def main(nx: float = 1200, ny: float = 800):
	j = np.tile(np.arange(0,ny,1),reps=(nx,1))
	i = np.tile(np.arange(0,nx,1),reps=(ny,1)).T

	lower_left_corner = vectorize(np.array((-2.0,-1.0,-1.0)))
	horizontal = vectorize(np.array((4.0,0,0)))
	vertical = vectorize(np.array((0.0,2,0)))
	origin = vectorize(np.array((0.0,0.0,0.0)))

	# print(i.shape)
	# print(j)
	u = coordinatize(i/nx)
	v = coordinatize(j/ny)

	r = ray(origin,lower_left_corner + u * horizontal + v * vertical)
	col = color(r)

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
