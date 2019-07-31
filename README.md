# PyTrace

![image2](./references/final_scene.png)

A (nearly) pure Ray Tracing Project for Python

This work is based off the books **[Ray Tracing in One Weekend](https://github.com/RayTracing/raytracinginoneweekend)** and **[Ray Tracing: the Next Week](https://github.com/RayTracing/raytracingthenextweek)** by Peter Shirley but ported to Python. 

This project seeks to expand past these previous works to become a more fully fledged path-tracer

#### To run, simply run pypy3 main.py or python main.py

dependencies include: 
1. pypy3 (note all other dependencies must be installed within pypy3)
2. numpy 
3. matplotlib
4. tqdm
5. noise

Technically, you can run w/o pypy3 installed but it is very slow w/o the JIT compilation, as seen below 

## Future Goals

1. Add more features such as different sampling methods, more materials, etc
2. Optimizations (Better BVH creation, memory and operation optimizations)
3. Arbitrary geometry support (mostly polygonal meshes)
4. Scene descriptions and parser
5. CUDA optimizations


## Benchmarks: 
Note: Iterations per second are how many output pixels are processed per second 
 
### W/ Cornell Box Rotated: 
2048 spp

800 x 800

Standard Implementation w/ PyPy

avg: 116.79 it/s

time: 1:31:19

### W/ Final Scene: 
2048 spp

800 x 800

Standard Implementaiton w/ Pypy

avg: N/A 

time: ~ 3 Hours

### W/ 3 Large spheres: 
256 spp 

1200 x 800 


Standard implementation

avg:  73.34 it/s 

time: 4:10:06

### W/ 3 Large spheres: 
256 spp 

1200 x 800 

Standard implementation w/PyPy

avg:  4953.02 it/s 

time: 00:03:13  

### W/ 3 Large spheres: 
100 spp 

200 x 100

Standard implementation

avg: 179.90 it/s

time: 00:01:50

### W/ 3 Large spheres: 
100 spp 

200 x 100 

Standard implementation w/ PyPy

avg: 10819.22 it/s

time: 00:00:01


### W/ 3 Large spheres + random spheres: 
256 spp 

1200 x 800 

Standard implementation w/PyPy

avg:  307.16 it/s

time: 00:52:01 

### W/ 3 Large spheres + random spheres:
64 spp

200 x 100 

Standard implementation w/PyPy w/o cprofile

avg: 1207.04it/s

time: 00:00:06


