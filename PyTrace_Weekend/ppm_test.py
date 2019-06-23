import sys
import os
import math
import random
from tqdm import tqdm
sys.path.append("./src/core/")
from geometry import * 
from hitable import * 
from shape import * 
from camera import * 

MAX_FLOAT = sys.float_info.max

def random_unit_sphere():
    p = vec3(1,1,1)
    while p.squared_length() >= 1.0:
        p = 2.0 * vec3(random.random(),random.random(),random.random()) - vec3(1.0,1.0,1.0)
        #print(p)
    #print(p)
    return p 


def color(r: ray, world: list,depth = 0,max_depth = 64):
    rec = hit_record()
    hit_anything,rec = iterate_hit_list(r,0.0,MAX_FLOAT,world)
    if (hit_anything and depth < max_depth):
        # print(rec.normal)
        target = rec.p + rec.normal + random_unit_sphere()
        depth += 1
        return 0.5 * color(ray(rec.p,target-rec.p),world,depth,max_depth)
    else:
        unit_direction = unit_vector(r.direction())
        t = 0.5 * (unit_direction.y() + 1.0)
        return (1.0 -t ) * vec3(1.0,1.0,1.0) + t * vec3(0.5,0.7,1.0)

def main(filename: str,output_res: tuple):
    f = open(filename + '.ppm','w')
    nx = output_res[0];
    ny = output_res[1];
    num_samples = 100
    f.write("P3\n" +  str(nx)  +  " "  + str(ny) + "\n255\n");

    hit_object_list = [] 
    hit_object_list.append(sphere(vec3(0,0,-1),0.5))
    hit_object_list.append(sphere(vec3(0,-100.5,-1),100))

    cam = camera()
    with tqdm(total = ny * nx) as pbar:
        for j in range(ny-1 ,0,-1):
            for i in range(0,nx):
                col = vec3(0,0,0)
                for s in range(0,num_samples):
                    u = float(i + random.random())/float(nx)
                    v = float(j + random.random())/float(ny)
                    r = cam.get_ray(u,v)
                    p = r(2.0)
                    col += color(r,hit_object_list)
                pbar.update(1)
                col /= float(num_samples)
                ir = int(255.99 * col.x0);
                ig = int(255.99 * col.x1);
                ib = int(255.99 * col.x2);
                f.write(str(ir)  +  " "  +  str(ig) +  " "  + str(ib) + "\n");
    f.close()
if  __name__ == "__main__":
    main("test",(200,100))

