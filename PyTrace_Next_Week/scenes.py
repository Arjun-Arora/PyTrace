import sys
import os
import math
import random
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

