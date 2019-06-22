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
	b = vec3(2,2,2)
	if a * 2 == a * b:
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
if __name__== "__main__":
	vec3_basic_add_test()
	vec3_basic_subtract_test()
	vec3_basic_negation_test()
	vec3_basic_iadd_test()
	vec3_basic_isub_test()
	vec3_basic_mult_test()
	vec3_basic_div_test()
	vec3_basic_neq_test()
	vec3_basic_pow_test()



