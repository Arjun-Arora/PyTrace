import numpy as np 

"""
functions here will be misc functions useful in other locations
"""

def unit_vector(vector):
	'''
	normalizes all 3-vectors in an array to be unit vectors
	'''
	assert(vector.shape[-1]) == 3

	length = (vector ** 2).sum(axis=-1) ** 0.5

	length = np.repeat(length[:,:,np.newaxis],3,axis=2)
	#print(length.shape)
	return_val = vector / length
	#print(return_val.shape)
	return return_val