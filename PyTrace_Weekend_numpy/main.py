import numpy as np
import matplotlib.pyplot as plt
import cython 

def main(nx: float = 200, ny: float = 100):
	j = np.tile(np.arange(0,ny,1),reps=(nx,1))
	i = np.tile(np.arange(0,nx,1),reps=(ny,1)).T
	print(i.shape)
	print(j)
	r = i/nx
	g = j /ny 
	b = np.ones_like(r) * 0.2 
	ir = 255.99 * r
	ig = 255.99 * g 
	ib = 255.99 * b
	output = np.dstack((ir,ig,ib))
	print(output.shape)
	plt.imshow(np.rot90(output.astype(int)))
	plt.show()
if __name__ == "__main__":
	main()
