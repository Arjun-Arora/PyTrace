from geometry import * 

class camera:
	def __init__(self):
		self.lower_left_corner = vec3(-2,-1,-1)
		self.horizontal = vec3(4,0,0)
		self.vertical = vec3(0,2,0)
		self.origin = vec3(0,0,0)
	def get_ray(self,u: float,v: float):
		return ray(self.origin,self.lower_left_corner + u * self.horizontal + v * self.vertical - self.origin)
