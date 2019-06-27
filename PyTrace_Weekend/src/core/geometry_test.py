from geometry import *

def vec3_basic_add_test():
	print("vec3_basic_add_test")
	a = vec3(3,4,6)
	b = vec3(2,2,1)
	c =  a + b
	if c == vec3(5,6,7):
		print("success!\n")
		return 1
	else:
		print("failed\n")
		return 0 

def vec3_basic_subtract_test():
	print("vec3_basic_subtract_test")
	a = vec3(3,4,6)
	b = vec3(4,4,7)
	c =  a - b
	if c == vec3(-1,0,-1):
		print("success!\n")
		return 1
	else:
		print("failed\n")
		return 0 
def vec3_basic_negation_test():
	print("vec3_basic_negation_test")
	a = vec3(3,4,6)
	if -a == vec3(-3,-4,-6):
		print("success!\n")
		return 1 
	else:
		print("failed\n")
		return 0 
def vec3_basic_iadd_test():
	print("vec3_basic_iadd_test")
	a = vec3(3,4,6)
	a += vec3(3,2,1)
	if (a == vec3(6,6,7)):
		print("success!\n")
		return 1
	else:
		print("failed\n")
		return 0 
def vec3_basic_isub_test():
	print("vec3_basic_isub_test")
	a = vec3(3,4,6)
	a -= vec3(3,2,1)
	if (a == vec3(0,2,5)):
		print("success!\n")
		return 1 
	else:
		print("failed\n")
		return 0 
def vec3_basic_mult_test():
	print("vec3_basic_mult_test")
	a = vec3(1,2,3)
	b = vec3(5,5,5)
	if a * 5 == a * b:
		print("success!\n")
		return 1
	else:
		print("failed\n")
		return 0 
def vec3_basic_rmult_test():
	print("vec3_basic_rmult_test")
	a = vec3(1,2,3)
	b = vec3(5,5,5)
	if a * 5 == a * b and 5 * a == a * b:
		print("success!\n")
		return 1
	else:
		print("failed\n")
		return 0 
def vec3_basic_div_test():
	print("vec3_basic_div_test")
	a = vec3(1,2,3)
	b = vec3(2,2,2)
	if a / 2 == a / b:
		print("success!\n")
		return 1
	else:
		print("failed\n")
		return 0 
def vec3_basic_idiv_test():
	print("vec3_basic_idiv_test")
	a = vec3(1,2,3)
	a /= 2
	if a == vec3(0.5,1,1.5):
		print("success!\n")
		return 1
	else:
		print("failed\n")
		return 0 
def vec3_basic_neq_test():
	print("vec3_basic_neq_test")
	a = vec3(3,4,6)
	b = vec3(3,4,7)
	if (a != b and not(a != a)):
		print("success!\n")
		return 1 
	else:
		print("failed\n")
		return 0
def vec3_basic_pow_test():
	print("vec3_basic_pow_test")
	a = vec3(2,4,6)
	b = 2
	c = vec3( 4,16,36)
	diff = (a ** b) - c 
	if diff.x0 <= 1e-6 and diff.x1 <= 1e-6 and diff.x2 <= 1e-6:
		print("success!\n")
		return 1
	else:
		print("failure\n")
		return 0
def vec3_basic_dot_test():
	print("vec3_basic_dot_test")
	a = vec3(1,2,3)
	b = vec3(2,4,6)
	c = a.dot(b)
	sol = 1 * 2 + 2 * 4 + 3 * 6
	if c == sol:
		print("success!\n")
		return 1
	else:
		print("failure\n")
		return 0
def vec3_basic_normalize_test():
	print("vec3_basic_normalize_test")
	x0,x1,x2 = 57,math.pi,6.7
	a = vec3(x0,x1,x2)
	a.normalize()
	norm =math.sqrt(x0 * x0 +  x1 * x1 + x2 * x2)
	if a == vec3(x0/norm,x1/norm,x2/norm):
		print("success!\n")
		return 1
	else:
		print("failure\n")
		return 0 
def vec3_basic_item_test():
	print("vec3_basic_item_test")
	a = vec3(2,4,6)
	if a[0] == 2 and a[1] == 4 and a[2] == 6:
		print("success!\n")
		return 1
	else:
		print("failure\n")
		return 0
def vec3_basic_set_item_test():
	print("vec3_basic_set_item_test")
	a = vec3(0,0,0)
	a[0] = 2 
	a[1] = 4
	a[2] = 6
	if a[0] == 2 and a[1] == 4 and a[2] == 6:
		print("success!\n")
		return 1
	else:
		print("failure\n")
		return 0
def unit_vector_basic_test():
	print("unit_vector_basic_test")
	a = vec3(3,6,9)
	length = a.length()
	a_unit = unit_vector(a)
	if a_unit == a/length:
		print('success!\n')
		return 1
	else:
		print('failure\n')
		return 0
def ray_basic_test_call():
	print("ray_basic_test_call")
	a = vec3(0,0,0)
	b = vec3(0,0,1)
	c = ray(a,b)
	output_ray = c(3)
	if output_ray == vec3(0,0,3):
		print('success!\n')
		return 1
	else:
		print('failure\n')
		return 0
if __name__== "__main__":
	vec3_basic_add_test()
	vec3_basic_subtract_test()
	vec3_basic_negation_test()
	vec3_basic_iadd_test()
	vec3_basic_isub_test()
	vec3_basic_mult_test()
	vec3_basic_rmult_test()
	vec3_basic_div_test()
	vec3_basic_idiv_test()
	vec3_basic_neq_test()
	vec3_basic_pow_test()
	vec3_basic_dot_test()
	vec3_basic_normalize_test()
	vec3_basic_item_test()
	vec3_basic_set_item_test()
	unit_vector_basic_test()
	ray_basic_test_call()


