import numpy as np


def main():
    nx = 200;
    ny = 100;
    print("P3\n" +  str(nx)  +  " "  + str(ny) + "\n255\n");
    for j in range(ny-1 ,0,-1):
        for i in range(0,nx):
            r =  float(i)/nx
            g = float(j)/ny
            b = 0.2
            ir = int(255.99 * r);
            ig = int(255.99 * g);
            ib = int(255.99 * b );
            print(str(ir)  +  " "  +  str(ig) +  " "  + str(ib) + "\n");

if  __name__ == "__main__":
    main()

