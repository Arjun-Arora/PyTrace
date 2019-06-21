import numpy as np


def main(filename: str,output_res: tuple):
    f = open(filename + '.txt','w')
    nx = output_res[0];
    ny = output_res[1];
    f.write("P3\n" +  str(nx)  +  " "  + str(ny) + "\n255\n");
    for j in range(ny-1 ,0,-1):
        for i in range(0,nx):
            r =  float(i)/nx
            g = float(j)/ny
            b = 0.2
            ir = int(255.99 * r);
            ig = int(255.99 * g);
            ib = int(255.99 * b );
            f.write(str(ir)  +  " "  +  str(ig) +  " "  + str(ib) + "\n");
    f.close()
if  __name__ == "__main__":
    main("test",(32,32))

