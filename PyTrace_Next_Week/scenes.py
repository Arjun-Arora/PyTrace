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
    # hit_object_list.append(box(vec3(130,0,65),vec3(295,165,230),mat_white))
    # hit_object_list.append(box(vec3(265,0,295),vec3(430,330,460),mat_white))
    # hit_object_list.append(translate(box(vec3(0, 0, 0), vec3(165, 165, 165), mat_white), vec3(130,0,65)))
    # hit_object_list.append(translate(box(vec3(0, 0, 0), vec3(165, 330, 165), mat_white), vec3(265,0,295)))
    hit_object_list.append(translate(rotate_y(box(vec3(0, 0, 0), vec3(165, 165, 165), mat_white),-18), vec3(130,0,65)))
    hit_object_list.append(translate(rotate_y(box(vec3(0, 0, 0), vec3(165, 330, 165), mat_white),15), vec3(265,0,295)))

    return hit_object_list

def cornell_smoke():
    hit_object_list = []
    mat_red = lambertian(constant_texture(vec3(0.65,0.05,0.05)))
    mat_white = lambertian(constant_texture(vec3(0.73,0.73,0.73)))
    mat_green = lambertian(constant_texture(vec3(0.12,0.45,0.15)))
    mat_light = diffuse_light(constant_texture(vec3(7,7,7)))

    hit_object_list.append(flip_normals(yz_rect(0,555,0,555,555,mat_green)))
    hit_object_list.append(yz_rect(0,555,0,555,0,mat_red))
    hit_object_list.append(xz_rect(113,443,127,432,554,mat_light))
    hit_object_list.append(flip_normals(xz_rect(0,555,0,555,555,mat_white)))
    hit_object_list.append(xz_rect(0,555,0,555,0,mat_white))
    hit_object_list.append(flip_normals(xy_rect(0,555,0,555,555,mat_white)))

    b1 = translate(rotate_y(box(vec3(0, 0, 0), vec3(165, 165, 165), mat_white),-18), vec3(130,0,65))
    b2 = translate(rotate_y(box(vec3(0, 0, 0), vec3(165, 330, 165), mat_white),15), vec3(265,0,295))
    medium1 = constant_medium(b1,0.01,constant_texture(vec3(1.0,1.0,1.0)))
    medium2 = constant_medium(b2,0.01,constant_texture(vec3(0.0,0.0,0.0)))
    hit_object_list.append(medium1)
    hit_object_list.append(medium2)

    return hit_object_list

def final_scene():
    nb = 5
    hit_object_list = []
    boxlist = []
    boxlist2 = []

    white = lambertian(constant_texture(vec3(0.73,0.73,0.73)))
    # bvh node test
    # ground = lambertian(constant_texture(vec3(0.48,0.83,0.53)))
    # for i in range(nb):
    #     for j in range(nb): 
    #         w = 100
    #         x0 = -1000 + i * w
    #         z0 = -1000 + j * w 
    #         y0 = 0 
    #         x1 = x0 + w
    #         y1 = 100 * (random.random() + 0.01)
    #         z1 = z0 + w
    #         boxlist.append(box(vec3(x0,y0,z0),vec3(x1,y1,z1),ground))

    # hit_object_list.append(bvh_node(boxlist,0,1))
    # bvh node test end

    # light test
    light = diffuse_light(constant_texture(vec3(7,7,7)))
    hit_object_list.append(xz_rect(123,423,147,412,554,light))
    # light test end

    # moving sphere test
    center = vec3(400,400,200)
    hit_object_list.append(moving_sphere(center,center + vec3(30,0,0),0,1,50,
                           lambertian(constant_texture(vec3(0.7,0.3,0.1)))))
    # moving sphere end

    # dielectric and metal test
    hit_object_list.append(sphere(vec3(260,150,45),50,dielectric(1.5)))
    hit_object_list.append(sphere(vec3(0,150,145),50,metal(vec3(0.8,0.8,0.8),10.0)))
    # dielectric and metal test end

    # constant medium test
    boundary = sphere(vec3(360,150,145),70,dielectric(1.5))
    hit_object_list.append(boundary)
    hit_object_list.append(constant_medium(boundary,0.2,constant_texture(vec3(0.2,0.4,0.9))))

    boundary2 = sphere(vec3(0,0,0),5000,dielectric(1.5))
    hit_object_list.append(constant_medium(boundary2,0.0001,constant_texture(vec3(1.0,1.0,1.0))))
    # constant medium test end

    # mapped texture test 
    earth_img = plt.imread("EarthMap.png")
    earth_img = np.swapaxes(earth_img,0,1)
    nx,ny,_ = earth_img.shape
    mat = lambertian(image_texture(earth_img,nx,ny))
    hit_object_list.append(sphere(vec3(400,200,400),100,mat))
    # mapped texture test end

    # perlin noise test
    pertext = noise_texture(0.1)
    hit_object_list.append(sphere(vec3(220,280,300),80,lambertian(pertext)))
    # perlin noise test end

    # rotate and translate and bvh node test
    # ns = 10
    # for j in range(ns):
    #     boxlist2.append(sphere(vec3(165 * random.random(),165 * random.random(),165 * random.random,10,white)))
    # hit_object_list.append(translate(rotate_y(bvh_node(boxlist2,0.0,1.0),15),vec3(-100,270,395)))
    # rotate and translate and bvh node test end 
    return hit_object_list




