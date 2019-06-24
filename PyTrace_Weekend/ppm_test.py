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
from material import * 

MAX_FLOAT = sys.float_info.max




def color(r: ray, world: list,depth = 0,max_depth = 4):
    rec = hit_record()
    hit_anything,rec = iterate_hit_list(r,0.001,MAX_FLOAT,world)
    if (hit_anything):
        # print(rec.normal)
        scattered = ray(vec3(0,0,0),vec3(0,0,0))
        attenuation = vec3(0,0,0)
        if_scatter,(scattered,attenuation) = rec.mat.scatter(r,rec)
        if (depth < max_depth and if_scatter):
            return attenuation * color( scattered,world,depth + 1,max_depth)
        else:
            return vec3(0.0,0.0,0.0)
    else:
        unit_direction = unit_vector(r.direction())
        t = 0.5 * (unit_direction.y() + 1.0)
        return (1.0 -t ) * vec3(1.0,1.0,1.0) + t * vec3(0.5,0.7,1.0)


def random_scene():
    hit_object_list = []
    hit_object_list.append(sphere(vec3(0,-1000,0),1000,lambertian(vec3(0.5,0.5,0.5))))
    # for a in range(-11,11,1):
    #     for b in range(-11,11,1):
    #         choose_mat = random.random()
    #         center = vec3(a + 0.9 * random.random(),0.2, b + 0.9 * random.random())
    #         if( (center-vec3(4,0.2,0)).length() > 0.9):
    #             if(choose_mat < 0.8): #diffuse
    #                 hit_object_list.append(sphere(center,0.2,
    #                                         lambertian(vec3(random.random() * random.random(),
    #                                                         random.random() * random.random(),
    #                                                         random.random() * random.random()))))
    #             elif(choose_mat < 0.95): #metal
    #                 hit_object_list.append(sphere(center,0.2,
    #                                               metal(vec3(0.5 * (1 + random.random()),
    #                                                          0.5 * (1 + random.random()),
    #                                                          0.5 * (1 + random.random())),
    #                                                          0.5 * random.random())))
    #             else:
    #                 hit_object_list.append(sphere(center,0.2,dielectric(1.5)))

    hit_object_list.append(sphere( vec3(0, 1, 0), 1.0, dielectric(1.5) ))
    hit_object_list.append(sphere( vec3(-4, 1, 0 ), 1.0, lambertian(vec3(0.4, 0.2, 0.1))))
    hit_object_list.append(sphere( vec3(4, 1, 0), 1.0, metal(vec3(0.7,0.6,0.5),0.0)))
    return hit_object_list

def main(filename: str,output_res: tuple):
    f = open(filename + '.ppm','w')
    nx = output_res[0];
    ny = output_res[1];
    num_samples = 256
    f.write("P3\n" +  str(nx)  +  " "  + str(ny) + "\n255\n");

    hit_object_list = [] 
    R = math.cos(math.pi/4)
    # hit_object_list.append(sphere(vec3(-R,0,-1),R,lambertian(vec3(0, 0, 1))))
    # hit_object_list.append(sphere(vec3(R,0,-1),R,lambertian(vec3(1, 0, 0))))
    # hit_object_list.append(sphere(vec3(0,0,-1),0.5,lambertian(vec3(0.1,0.2,0.5))))
    # hit_object_list.append(sphere(vec3(0,-100.5,-1),100,lambertian(vec3(0.8,0.8,0.0))))
    # hit_object_list.append(sphere(vec3(1,0,-1),0.5,metal(vec3(0.8,0.6,0.2))))
    # hit_object_list.append(sphere(vec3(-1,0,-1),0.5,dielectric(1.5)))
    # hit_object_list.append(sphere(vec3(-1,0,-1),-0.45,dielectric(1.5)))
    hit_object_list = random_scene()
    #print("hit this")
    lookfrom = vec3(13,2,3)
    lookat = vec3(0,0,0)
    dist_to_focus = 10
    aperture = 0.1

    cam = camera(lookfrom,lookat,vec3(0,1,0),20,float(nx)/float(ny),aperture,dist_to_focus)
    with tqdm(total = ny * nx) as pbar:
        for j in range(ny-1 ,0,-1):
            for i in range(0,nx):
                col = vec3(0,0,0)
                for s in range(0,num_samples):
                    u = float(i + random.random())/float(nx)
                    v = float(j + random.random())/float(ny)
                    r = cam.get_ray(u,v)
                    #p = r(2.0)
                    col += color(r,hit_object_list,0)
                pbar.update(1)
                col /= float(num_samples)
                col = vec3(math.sqrt(col[0]),math.sqrt(col[1]),math.sqrt(col[2]))
                ir = int(255.99 * col.x0);
                ig = int(255.99 * col.x1);
                ib = int(255.99 * col.x2);
                f.write(str(ir)  +  " "  +  str(ig) +  " "  + str(ib) + "\n");
    f.close()
if  __name__ == "__main__":
    main("test",(1200,800))

