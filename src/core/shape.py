import sys
from hitable import * 
import math
from geometry import *
from material import * 
FLT_MAX = sys.float_info.max
import random

K_EPSILON = 1e-6



def get_sphere_uv(p: vec3):
    phi = atan2(p[2],p[0])
    theta = asin(p[1])
    u = 1 - (phi + pi)/ (2 * pi )
    v = (theta + pi / 2) / ( pi )
    return u,v

class sphere(hitable):
    def __init__(self,center: vec3,radius: float,mat: material):
        self.center = center
        self.radius = radius
        self.mat = mat
    def hit(self,r: ray , t_min: float,t_max: float):
        rec = hit_record()
        rec.mat = self.mat
        oc = r.origin - self.center
        a = (r.direction).dot(r.direction)
        b = oc.dot(r.direction)
        c = oc.dot(oc) - (self.radius * self.radius)
        discriminant = b * b - (a * c)
        if (discriminant > 0 ): 
            temp = (-b - math.sqrt(b * b - a * c))/a
            if ((temp < t_max and temp > t_min)):
                #print('hit this')
                rec.t = temp
                rec.p = r(rec.t)
                rec.u,rec.v = get_sphere_uv((rec.p-self.center)/self.radius)
                rec.normal = (rec.p - self.center)/self.radius
                return (True, rec)
            temp = (-b + math.sqrt(b * b - a * c))/a
            if ((temp < t_max and temp > t_min)):
                #print('hit this')
                rec.t = temp
                rec.p = r(rec.t)
                rec.u,rec.v = get_sphere_uv((rec.p-self.center)/self.radius)
                rec.normal = (rec.p - self.center)/self.radius
                return (True, rec)
        # print('got here with discriminant: {}'.format(discriminant))
        return (False,rec)
    def bounding_box(self, t0: float=None, t1: float=None):
        box = aabb(self.center - vec3(self.radius,self.radius,self.radius),
                  self.center + vec3(self.radius,self.radius,self.radius))
        return (True,box);




class moving_sphere(hitable):
    def __init__(self,cen0: vec3, cen1: vec3, t0: float, t1: float, r: float, mat: material):
        self.center0 = cen0
        self.center1 = cen1
        self.time0 = t0
        self.time1 = t1
        self.radius = r 
        self.mat = mat
    def curr_center(self,time: float):
        return self.center0 + ((time - self.time0)/(self.time1-self.time0)) * (self.center1 - self.center0)

    def hit(self,r: ray , t_min: float,t_max: float):
        rec = hit_record()
        rec.mat = self.mat
        #oc = r.origin - self.center
        oc = r.origin - self.curr_center(r.time)
        a = (r.direction).dot(r.direction)
        b = oc.dot(r.direction)
        c = oc.dot(oc) - (self.radius * self.radius)
        discriminant = b * b - (a * c)
        if (discriminant > 0 ): 
            temp = (-b - math.sqrt(b * b - a * c))/a
            if ((temp < t_max and temp > t_min)):
                rec.t = temp
                rec.p = r(rec.t)
                #rec.normal = (rec.p - self.center)/self.radius
                rec.normal = (rec.p - self.curr_center(r.time))/self.radius
                return (True, rec)
            temp = (-b + math.sqrt(b * b - a * c))/a
            if ((temp < t_max and temp > t_min)):
                #print('hit this')
                rec.t = temp
                rec.p = r(rec.t)
                #rec.normal = (rec.p - self.center)/self.radius
                rec.normal = (rec.p - self.curr_center(r.time))/self.radius
                return (True, rec)
        return (False,rec)
    def bounding_box(self, t0: float, t1: float):
        box = sorrounding_box(sphere(self.curr_center(t0),self.radius,self.mat).bounding_box()[1],
                              sphere(self.curr_center(t1),self.radius,self.mat).bounding_box()[1])
        return (True,box)


'''
x-y axis aligned rectangle
'''
class xy_rect(hitable):
    def __init__(self,x0: float, x1: float, y0: float, y1: float, k: float, mat: material):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.k = k 
        self.mat = mat 
    def hit(self,r: ray , t0: float,t1: float):
        rec = hit_record()
        rec.mat = self.mat
        t = (self.k - r.origin[2]) / r.direction[2]
        if t < t0 or t > t1:
            return (False,rec)
        x = r.origin[0] + t * r.direction[0]
        y = r.origin[1] + t * r.direction[1]
        if x < self.x0 or x > self.x1 or y < self.y0 or y > self.y1: 
            return (False,rec)
        rec.u = (x-self.x0)/(self.x1-self.x0)
        rec.v = (y-self.y0)/(self.y1-self.y0)
        rec.t = t 
        rec.p = r(rec.t)
        rec.normal = vec3(0,0,1)
        return (True,rec)
    def bounding_box(self,t0: float, t1: float ): 
        box = aabb(vec3(self.x0,self.y0,self.k-0.0001),vec3(self.x1,self.y1,self.k + 0.0001))
        return (True,box)

'''
x-z axis aligned rectangle
'''
class xz_rect(hitable):
    def __init__(self,x0: float, x1: float, z0: float, z1: float, k: float, mat: material):
        self.x0 = x0
        self.x1 = x1
        self.z0 = z0
        self.z1 = z1
        self.k = k 
        self.mat = mat 
    def hit(self,r: ray , t0: float,t1: float):
        rec = hit_record()
        rec.mat = self.mat
        t = (self.k - r.origin[1]) / r.direction[1]
        if t < t0 or t > t1:
            return (False,rec)
        x = r.origin[0] + t * r.direction[0]
        z = r.origin[2] + t * r.direction[2]
        if x < self.x0 or x > self.x1 or z < self.z0 or z > self.z1: 
            return (False,rec)
        rec.u = (x-self.x0)/(self.x1-self.x0)
        rec.v = (z-self.z0)/(self.z1-self.z0)
        rec.t = t 
        rec.p = r(rec.t)
        rec.normal = vec3(0,1,0)
        return (True,rec)
    def bounding_box(self,t0: float, t1: float ): 
        box = aabb(vec3(self.x0,self.k-0.0001,self.z0),vec3(self.x1,self.k + 0.0001,self.z1))
        return (True,box)


'''
y-z axis aligned rectangle
'''
class yz_rect(hitable):
    def __init__(self,y0: float, y1: float, z0: float, z1: float, k: float, mat: material):
        self.y0 = y0
        self.y1 = y1
        self.z0 = z0
        self.z1 = z1
        self.k = k 
        self.mat = mat 
    def hit(self,r: ray , t0: float,t1: float):
        rec = hit_record()
        rec.mat = self.mat
        t = (self.k - r.origin[0]) / r.direction[0]
        if t < t0 or t > t1:
            return (False,rec)
        y = r.origin[1] + t * r.direction[1]
        z = r.origin[2] + t * r.direction[2]
        if y < self.y0 or y > self.y1 or z < self.z0 or z > self.z1: 
            return (False,rec)
        rec.u = (y-self.y0)/(self.y1-self.y0)
        rec.v = (z-self.z0)/(self.z1-self.z0)
        rec.t = t 
        rec.p = r(rec.t)
        rec.normal = vec3(1,0,0)
        return (True,rec)
    def bounding_box(self,t0: float, t1: float ): 
        box = aabb(vec3(self.k-0.0001,self.y0,self.z0),vec3(self.k + 0.0001,self.y1,self.z1))
        return (True,box)


'''
box shape, constructed from a series of rects as well as their flipped normal counterparts
'''

class box(hitable):
    def __init__(self,p0: vec3, p1: vec3, mat: material):
        self.pmin = p0
        self.pmax = p1
        self.mat = mat
        hit_object_list = []
        hit_object_list += [xy_rect(p0[0],p1[0],p0[1],p1[1],p1[2],mat)]
        hit_object_list += [flip_normals(xy_rect(p0[0],p1[0],p0[1],p1[1],p0[2],mat))]
        hit_object_list += [xz_rect(p0[0],p1[0],p0[2],p1[2],p1[1],mat)]
        hit_object_list += [flip_normals(xz_rect(p0[0],p1[0],p0[2],p1[2],p0[1],mat))]
        hit_object_list += [yz_rect(p0[1],p1[1],p0[2],p1[2],p1[0],mat)]
        hit_object_list += [flip_normals(yz_rect(p0[1],p1[1],p0[2],p1[2],p0[0],mat))]
        self.hit_list = hitable_list(hit_object_list)
    def hit(self,r: ray , t0: float,t1: float):
        return self.hit_list.hit(r,t0,t1)
    def bounding_box(self,t0: float, t1: float):
        box = aabb(self.pmin,self.pmax)
        return (True,box)

class constant_medium(hitable):
    def __init__(self,b: hitable, d: float, a: texture):
        self.boundary = b
        self.density  = d 
        self.phase_function = isotropic(a)
    def hit(self, r: ray, t_min: float, t_max: float):
        return_rec = hit_record()
        is_hit1,rec1 = self.boundary.hit(r,-FLT_MAX,FLT_MAX)
        if is_hit1:
            is_hit2,rec2 = self.boundary.hit(r,rec1.t + 0.0001,FLT_MAX)
            if is_hit2:
                if rec1.t < t_min:
                    rec1.t = t_min
                if rec2.t > t_max:
                    rec2.t = t_max
                if rec1.t >= rec2.t:
                    return (False,return_rec)
                if rec1.t < 0:
                    rec1.t = 0
                distance_inside_boundary = (rec2.t - rec1.t) * r.direction.length()
                hit_distance = -(1/self.density) * math.log(random.random())
                if hit_distance < distance_inside_boundary:
                    return_rec.t = rec1.t + hit_distance/r.direction.length()
                    return_rec.p = r(return_rec.t)
                    return_rec.normal = vec3(1.0,0,0) #arbitrary
                    return_rec.mat = self.phase_function
                    return (True,return_rec)
        return (False,return_rec)

class triangle(hitable): 
    def __init__(self,v0: vec3, v1: vec3, v2: vec3,mat: material):
        self.v0 = v0
        self.v1 = v1 
        self.v2 = v2
        self.mat = mat
        self.normal = ((self.v1 - self.v0).cross(self.v2 - self.v0)).normalize()
    def hit(self,r: ray , t0: float,t1: float):
        rec = hit_record()

        # Moller Trumbore algo
        e1 = self.v1 - self.v0
        e2 = self.v2 - self.v0 
        s = r.origin - self.v0 
        s1 = r.direction.cross(e2)
        s2 = s.cross(e1)

        Det = s1.dot(e1)
        invDet = 1 /Det

        if Det < K_EPSILON:
            return (False,rec)
        if abs(Det) < K_EPSILON:
            return (False,rec)

        t_u_v = invDet * vec3(s2.dot(e2),s1.dot(s),s2.dot(r.direction))
        t = t_u_v[0]
        u = t_u_v[1]
        v = t_u_v[2]

        if u < 0 or u > 1: 
            return (False,rec)
        if v < 0 or u + v > 1:
            return (False,rec)

        #print("{} {} ".format(self.normal.dot(e1),self.normal.dot(e2)))
        #print(self.normal.length())
        rec.u = u
        rec.v = v
        rec.t = t 
        rec.p = r(rec.t)
        rec.normal = self.normal
        rec.mat = self.mat
        # print(t)
        #print(rec.mat)
        #print("{} {}".format(rec.u,rec.v))

        return (True,rec)
    def bounding_box(self,t0: float, t1: float ):
        min_x = min([self.v0[0],self.v1[0],self.v2[0]])
        max_x = max([self.v0[0],self.v1[0],self.v2[0]])

        min_y = min([self.v0[1],self.v1[1],self.v2[1]])
        max_y = max([self.v0[1],self.v1[1],self.v2[1]])

        min_z = min([self.v0[2],self.v0[2],self.v2[2]])
        max_z = max([self.v0[2],self.v0[2],self.v2[2]])

        box = aabb(vec3(min_x,min_y,min_z),vec3(max_x,max_y,max_z)) 
        return (True,box)


























