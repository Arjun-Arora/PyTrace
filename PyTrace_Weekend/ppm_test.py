import sys
import os
sys.path.append("./src/core/")
from geometry import * 
from hitable import * 
from shape import * 
import math

MAX_FLOAT = sys.float_info.max

def color(r: ray, world: list):
    rec = hit_record()
    hit_anything,rec = iterate_hit_list(r,0.0,MAX_FLOAT,world)
    if (hit_anything):
        # print(rec.normal)
        return 0.5 * vec3(rec.normal.x() + 1, rec.normal.y() + 1,rec.normal.z() + 1)
    else:
        unit_direction = unit_vector(r.direction())
        t = 0.5 * (unit_direction.y() + 1.0)
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

    hit_object_list = [] 
    hit_object_list.append(sphere(vec3(0,0,-1),0.5))
    hit_object_list.append(sphere(vec3(0,-100.5,-1),100))
    #hit_object_list.append(sphere(vec3(2,2,-3),1))
    # print(new_list.hit_list)


    for j in range(ny-1 ,0,-1):
        for i in range(0,nx):
            u =  float(i)/float(nx)
            v = float(j)/float(ny)
            r = ray(origin,lower_left_corner + u * horizontal + v * vertical)

            p = r(2.0)
            col = color(r,hit_object_list)
            ir = int(255.99 * col.x0);
            ig = int(255.99 * col.x1);
            ib = int(255.99 * col.x2);
            f.write(str(ir)  +  " "  +  str(ig) +  " "  + str(ib) + "\n");
    f.close()
if  __name__ == "__main__":
    main("test",(200,100))

