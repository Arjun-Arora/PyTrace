import sys
import os
import math
import random
from tqdm import tqdm

from scenes import * 
sys.path.append("./src/core/")
from geometry import * 
from hitable import * 
from shape import * 
from camera import * 
from material import * 
from texture import * 
from sampler import * 
import numpy as np
import matplotlib.pyplot as plt
import cProfile
MAX_FLOAT = sys.float_info.max

def color(r: ray, world: list,depth = 0,max_depth = 4):
    rec = hit_record()
    hit_anything,rec = hitable_list(world).hit(r,0.001,MAX_FLOAT)
    if (hit_anything):
        # print(rec.normal)
        scattered = ray(vec3(0,0,0),vec3(0,0,0),0.0)
        attenuation = vec3(0,0,0)
        if_scatter,(scattered,attenuation) = rec.mat.scatter(r,rec)
        emitted = rec.mat.emitted(rec.u,rec.v,rec.p)
        if (depth < max_depth and if_scatter):
            #print(color( scattered,world,depth + 1,max_depth))
            return emitted + attenuation * color( scattered,world,depth + 1,max_depth)
        else:
            return emitted
    else:
        #placeholder until fully implemented lights
        # return vec3(1,1,1)
        # unit_direction = unit_vector(r.direction)
        # t = 0.5 * (unit_direction.y() + 1.0)
        # return (1.0 -t ) * vec3(1.0,1.0,1.0) + t * vec3(0.5,0.7,1.0)

        return vec3(0,0,0)


def main(filename: str = 'output',output_res: tuple = (200,100),num_samples= 100):
    nx = output_res[0];
    ny = output_res[1];
    num_samples = num_samples

    output = np.zeros((nx,ny,3)).tolist()

    #f.write("P3\n" +  str(nx)  +  " "  + str(ny) + "\n255\n");

    hit_object_list = [] 
    R = math.cos(math.pi/4)

    #hit_object_list = random_scene()
    #hit_object_list = two_spheres()
    #hit_object_list = two_perlin_spheres()
    #hit_object_list = earth_sphere()
    #hit_object_list = simple_light()
    hit_object_list = cornell_box()
    #hit_object_list = cornell_smoke()
    #hit_object_list = final_scene()
    #lookfrom = vec3(13,2,3)
    #lookat = vec3(0,0,0)

    #lookfrom = vec3(13,2,10)
    #lookat = vec3(0,2,0)

    # dist_to_focus = 10
    # aperture = 0.1
    #vfov = 20
    lookfrom = vec3(278,278,-800)
    #lookfrom = vec3(478,278,-600)
    lookat = vec3(278,278,0)
    dist_to_focus = 10
    aperture = 0 
    vfov = 40
    seed = 123

    sampler = uniform_sampler_2D(seed)
    #sampler = stratified_sampler_2D(num_samples,seed)
    cam = camera(lookfrom,lookat,vec3(0,1,0),vfov,float(nx)/float(ny),aperture,dist_to_focus,0.0,1.0)
    with tqdm(total = ny * nx) as pbar:
        for j in range(ny-1 ,-1,-1):
            for i in range(0,nx):
                col = vec3(0,0,0)
                samples = sampler.generate_n_samples_uv(num_samples)
                for s in samples: 
                    u,v = s
                    #print(" i: {} u:{} j: {}, v: {} ".format(i,u,j,v))
                    s = (i + u)/nx
                    t = (j + v)/ny
                    r = cam.get_ray(s,t)
                    col += color(r,hit_object_list,0)
                col /= float(num_samples)
                #col = vec3(math.sqrt(col[0]),math.sqrt(col[1]),math.sqrt(col[2]))
                ir = 255.99 * math.sqrt(col[0]);
                ig = 255.99 * math.sqrt(col[1]);
                ib = 255.99 * math.sqrt(col[2]);

                ir = (max(0,min(ir,255)))
                ig = (max(0,min(ig,255)))
                ib = (max(0,min(ib,255)))
                output[i][j] = [ir,ig,ib]

                pbar.update(1)
                #f.write(str(ir)  +  " "  +  str(ig) +  " "  + str(ib) + "\n");

    plt.imsave(filename + ".png",np.rot90(np.array(output)).astype(np.uint8))
    #f.close()

if  __name__ == "__main__":
    #cProfile.runctx('main()',None,("random_spheres",(200,100),64))
    #main("./unit_tests/random_spheres_unit_test",(200,100),64)
    #main("./test",output_res = (400,300),num_samples = 1024)
    #main("./test",output_res = (800,800),num_samples = 2048)
    main("./test",output_res = (256,192),num_samples = 256)
    # 00:00:43 1118.0 it/s


