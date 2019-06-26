import numpy as np 

"""
functions here will be misc functions useful in other locations
"""

def coordinatize(arr):
	'''
	converts coordinate array of mxn to be m x n x 1
	'''
	return arr[:,:,None]
def vectorize(vector):
	'''
	converts vector of 3, to be of 1 x 1 x 3
	'''
	return vector[None,None,:]
def unit_vector(vector):
	'''
	normalizes all 3-vectors in an array to be unit vectors
	'''
	assert(vector.shape[-1]) == 3

	length = (vector ** 2).sum(axis=-1) ** 0.5
	print(vector.shape)
	length = np.repeat(length[:,:,np.newaxis],3,axis=2)
	print(length.shape)
	return_val = vector / length
	#print(return_val.shape)
	return return_val