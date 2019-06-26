import numpy as np 

"""
functions here will be misc functions useful in other locations
"""

def tile(arr: np.ndarray):
	'''
	converts array of mxn to be a tile of shape m x n x 1
	'''
	#assert(len(arr.shape),2)
	if len(arr.shape) == 2:
		return arr[:,:,None]
	elif len(arr.shape == 3):
		return arr
	else:
		return None
def vec3(x0,x1,x2):
	'''
	converts 3 values to be a tile of shape 1 x 1 x 3, also known as a vec3
	also converts 2D arrays to be a tile of shape m x n x 3 , also known as a tile of vec3 
	'''
	if isinstance(x0,np.ndarray) and isinstance(x1,np.ndarray) and isinstance(x2,np.ndarray) and len(x0.shape)==2:
		return np.dstack((x0,x1,x2))
	else:
		return np.array((x0,x1,x2))[None,None,:]

def tiledot(tile_0,tile_1):
	'''
	applies dot product across 3 dimension of a tile
	'''
	assert(len(tile_0.shape)==3)
	assert(len(tile_1.shape)==3)
	return_val = np.sum(tile_0 * tile_1,axis=-1)
	return return_val

def unit_vector(vector: np.ndarray):
	'''
	normalizes all 3-vectors in a tile to be unit vectors
	'''
	assert(vector.shape[-1]) == 3

	length = (vector ** 2).sum(axis=-1) ** 0.5
	#print(vector.shape)
	length = np.repeat(length[:,:,np.newaxis],3,axis=2)
	#print(length.shape)
	return_val = vector / length
	#print(return_val.shape)
	return return_val