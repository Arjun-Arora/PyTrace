import sys
import os
import math
import random
import matplotlib.pyplot as plt
import numpy as np 
sys.path.append("./src/core/")
from geometry import * 
from hitable import * 
from shape import * 
from camera import * 
from material import * 
from texture import * 

#define scenes here
# TODO: make scenes.py a parser with a text scenefile input 

def random_scene():
    hit_object_list = []
    checker = checker_texture(constant_texture(vec3(0.2,0.3,0.1)), constant_texture(vec3(0.9,0.9,0.9)))
    hit_object_list.append(sphere(vec3(0,-1000,0),1000,lambertian(checker)))
    for a in range(-10,10,1):
        for b in range(-10,10,1):
            choose_mat = random.random()
            center = vec3(a + 0.9 * random.random(),0.2, b + 0.9 * random.random())
            if( (center-vec3(4,0.2,0)).length() > 0.9):
                if(choose_mat < 0.8): #diffuse
                    hit_object_list.append(moving_sphere(center,center + vec3(0,0.5 * random.random(),0),
                                            0.0,1.0,0.2,
                                            lambertian(constant_texture(vec3(random.random() * random.random(),
                                                                            random.random() * random.random(),
                                                                            random.random() * random.random())))))
                elif(choose_mat < 0.95): #metal
                    hit_object_list.append(sphere(center,0.2,
                                                  metal(vec3(0.5 * (1 + random.random()),
                                                             0.5 * (1 + random.random()),
                                                             0.5 * (1 + random.random())),
                                                             0.5 * random.random())))
                else:
                    hit_object_list.append(sphere(center,0.2,dielectric(1.5)))

    hit_object_list.append(sphere( vec3(0, 1, 0), 1.0, dielectric(1.5) ))
    hit_object_list.append(sphere( vec3(-4, 1, 0 ), 1.0, lambertian(constant_texture(vec3(0.4, 0.2, 0.1)))))
    hit_object_list.append(sphere( vec3(4, 1, 0), 1.0, metal(vec3(0.7,0.6,0.5),0.0)))
    return hit_object_list

def two_spheres():
    hit_object_list = []
    checker = checker_texture(constant_texture(vec3(0.2,0.3,0.1)), constant_texture(vec3(0.9,0.9,0.9)))
    bottom_sphere = sphere(vec3(0,-10,0),10,lambertian(checker))
    top_sphere = sphere(vec3(0,10,0),10,lambertian(checker))
    hit_object_list += [bottom_sphere,top_sphere]
    return hit_object_list

def two_perlin_spheres():
    hit_object_list = []
    pertext = noise_texture()
    bottom_sphere = sphere(vec3(0,-1000,0),1000,lambertian(pertext))
    top_sphere = sphere(vec3(0,2,0),2,lambertian(pertext))
    hit_object_list += [bottom_sphere,top_sphere]

    return hit_object_list

def earth_sphere():
    hit_object_list = []
    earth_img = plt.imread("EarthMap.png")
    earth_img = np.swapaxes(earth_img,0,1)
    nx,ny,_ = earth_img.shape
    mat = lambertian(image_texture(earth_img,nx,ny))
    #other_mat = lambertian(constant_texture(vec3(0.2,0.3,0.1)))
    new_sphere = sphere(vec3(0,0,0),2.0,mat)
    hit_object_list += [new_sphere]

    return hit_object_list

def simple_light():
    hit_object_list = []
    pertext = noise_texture(4)
    hit_object_list.append(sphere(vec3(0,-1000,0),1000,lambertian(pertext)))
    hit_object_list.append(sphere(vec3(0,2,0),2,lambertian(pertext)))
    light_color = constant_texture(vec3(4.0,4.0,4.0))
    hit_object_list.append(sphere(vec3(0,7,0),2,diffuse_light(light_color)))
    hit_object_list.append(xy_rect(3,5,1,3,-2,diffuse_light(light_color)))

    return hit_object_list

def cornell_box():
    hit_object_list = []
    mat_red = lambertian(constant_texture(vec3(0.65,0.05,0.05)))
    mat_white = lambertian(constant_texture(vec3(0.73,0.73,0.73)))
    mat_green = lambertian(constant_texture(vec3(0.12,0.45,0.15)))
    mat_light = diffuse_light(constant_texture(vec3(15,15,15)))

    hit_object_list.append(flip_normals(yz_rect(0,555,0,555,555,mat_green)))
    hit_object_list.append(yz_rect(0,555,0,555,0,mat_red))
    hit_object_list.append(xz_rect(213,343,227,332,554,mat_light))
    hit_object_list.append(flip_normals(xz_rect(0,555,0,555,555,mat_white)))
    hit_object_list.append(xz_rect(0,555,0,555,0,mat_white))
    hit_object_list.append(flip_normals(xy_rect(0,555,0,555,555,mat_white)))
    hit_object_list.append(box(vec3(130,0,65),vec3(295,165,230),mat_white))
    hit_object_list.append(box(vec3(265,0,295),vec3(430,330,460),mat_white))

    return hit_object_list



