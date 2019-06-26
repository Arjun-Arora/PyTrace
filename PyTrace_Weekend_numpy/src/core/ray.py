import numpy as np

class ray:
	def __init__(self,origin: np.ndarray,direction: np.ndarray):

		#ensure that we are dealing with stacked 3 vectors
		assert(origin.shape[-1] == 3)
		assert(direction.shape[-1] == 3)
		self.a = origin
		self.b = direction
	def origin(self):
		return self.a
	def direction(self):
		return self.b
	def __call__(self,t):
		return self.a + t * self.b