# PyTrace

![image](./PyTrace_Next_Week/references/cornell_box_rotated.png)


A (nearly) pure Ray Tracing Project for Python

This work is based off the books **Ray Tracing in One Weekend** and **Ray Tracing: the Next Week** by Peter Shirley but ported to Python 

The original code for each book I wrote is contained within the sub directories **PyTrace_Weekend** and **PyTrace_Next_Week**

main.py includes all configurations you need to generate an image. 

to run, simply run pypy3 main.py or python main.py

dependencies include: 
1. pypy3
2. numpy 
3. matplotlib
4. tqdm
5. noise

Technically, you can run w/o pypy3 installed but it is very slow w/o the JIT compilation, as seen below 

Will look to accelerate with CUDA compilation in the future


## PyTrace_Next_Week Benchmark: 
Note: Iterations per second are how many pixels 
 
### W/ Cornell Box Rotated: 
2048 spp

800 x 800

Standard Implementation w/ Pypy

avg: 116.79 it/s

time: 1:31:19

### W/ Final Scene: 
2048 spp

800 x 800

Standard Implementaiton w/ Pypy

avg: N/A 

time: ~ 3 Hours

## PyTrace_Weekend Benchmark:
Note: Iterations per second are how many pixels 

### W/ current scene: 
256 spp 

1200 x 800 

3 Large spheres

Standard implementation

avg:  73.34 it/s 

time: 4:10:06

### W/ current scene: 
256 spp 

1200 x 800 

3 Large spheres

Standard implementation w/PyPy

avg:  4953.02 it/s 

time: 00:03:13   

### W/ current scene: 
100 spp 

200 x 100

3 Large spheres

Standard implementation

avg: 179.90 it/s

time: 00:01:50

### W/ current scene
100 spp 

200 x 100 

3 Large spheres

Standard implementation w/ PyPy

avg: 10819.22 it/s

time: 00:00:01


### W/ random scene: 
256 spp 

1200 x 800 

3 Large spheres + random spheres

Standard implementation w/PyPy

avg:  307.16 it/s

time: 00:52:01 

### W/ random scene:
64 spp

200 x 100 

3 Large spheres + random spheres

Standard implementation w/PyPy w/o cprofile

avg: 1207.04it/s

time: 00:00:06


### W/ random scene:
200 x 100 

3 Large spheres + random spheres

Standard implementation w/PyPy w/ cprofile

time: 151.181 seconds


