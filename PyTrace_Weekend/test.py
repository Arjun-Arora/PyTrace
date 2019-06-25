import sys
import os
import math
import random
from tqdm import tqdm
sys.path.append("./src/core/")
from geometry import * 

if  __name__ == "__main__":
	x0 = np.array((1,2)) * 2 
	b = vec3((2.0,1,0))
	# x1 = np.array((2,3))
	# x2 = np.array((3,4))
	# a = vec3((x0,x1,x2))
	# print(a)
	# print(a.arr.shape)
	print(x0)
	print(b)
	print(b * x0 )