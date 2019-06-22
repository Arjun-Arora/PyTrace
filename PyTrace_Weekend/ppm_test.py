import sys
import os
sys.path.append("./src/core/")
from geometry import * 
import numpy as np
import math
#defined with right handed coordinate system
def hit_sphere (center,radius,ray):
    oc = ray.origin() - center
    a = (ray.direction()).dot(ray.direction())
    b = 2.0 * oc.dot(ray.direction())
    c = oc.dot(oc) - radius * radius
    discriminant = b * b - 4 * a * c
    if (discriminant < 0):
        return -1.0
    else:
        return (-b - math.sqrt(discriminant))/(2.0 * a)
def color(r): 
    t = hit_sphere(vec3(0,0,-1),0.5,r)
    if (t > 0):
        N = unit_vector(r(t) - vec3(0,0,-1))
        return 0.5 * vec3(N.x()+1,N.y() + 1, N.z() + 1)
    
    unit_direction = unit_vector(r.direction())
    t = 0.5 * (unit_direction.y() + 1.0 )
    return (1.0 -t ) * vec3(1.0,1.0,1.0) + t * vec3(0.5,0.7,1.0)

def main(filename: str,output_res: tuple):
    f = open(filename + '.ppm','w')
    nx = output_res[0];
    ny = output_res[1];
    f.write("P3\n" +  str(nx)  +  " "  + str(ny) + "\n255\n");

    lower_left_corner = vec3(-2.0,-1.0,-1.0)
    horizontal = vec3(4.0,0,0)
    vertical = vec3(0,2,0)
    origin = vec3(0,0,0)
    for j in range(ny-1 ,0,-1):
        for i in range(0,nx):
            u =  float(i)/float(nx)
            v = float(j)/float(ny)
            r = ray(origin,lower_left_corner + u * horizontal + v * vertical)
            col = color(r)
            ir = int(255.99 * col.x0);
            ig = int(255.99 * col.x1);
            ib = int(255.99 * col.x2);
            f.write(str(ir)  +  " "  +  str(ig) +  " "  + str(ib) + "\n");
    f.close()
if  __name__ == "__main__":
    main("test",(200,100))

