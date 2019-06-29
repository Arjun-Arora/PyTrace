Ray Tracing Project for Python

Purely for educational purposes

First will work through Ray Tracing on a weekend, contained here

Then will work on my own implementation 


Will look to accelerate with CUDA compilation in the future

PyTrace_Weekend Benchmark:
Note: Iterations per second are how many pixels 

W/ current scene: 
256 spp 
1200 x 800 
3 Large spheres
Standard implementation
avg:  73.34 it/s 
time: 4:10:06

W/ current scene: 
256 spp 
1200 x 800 
3 Large spheres
Standard implementation w/PyPy
avg:  4953.02 it/s 
time: 00:03:13   

W/ current scene: 
100 spp 
200 x 100
3 Large spheres
Standard implementation
avg: 179.90 it/s
time: 00:01:50

W/ current scene
100 spp 
200 x 100 
3 Large spheres
Standard implementation w/ PyPy
avg: 10819.22 it/s
time: 00:00:01


W/ random scene: 
256 spp 
1200 x 800 
3 Large spheres + random spheres
Standard implementation w/PyPy
avg:  307.16 it/s
time: 00:52:01 

W/ random scene:
64 spp
200 x 100 
3 Large spheres + random spheres
Standard implementation w/PyPy w/o cprofile
avg: 1207.04it/s
time: 00:00:


W/ random scene:
64 spp
200 x 100 
3 Large spheres + random spheres
Standard implementation w/PyPy w/ cprofile
time: 237.142 seconds


