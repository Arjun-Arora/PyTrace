import geometry 

def vec3_basic_add_test():
    a = geometry.vec3(3,4,6)
    b = geometry.vec3(2,2,1)
    c =  a + b
    print(a)
    print("\n + \n")
    print(b)
    print("\n = \n")
    print(c)

if __name__== "__main__":
    vec3_basic_add_test()

