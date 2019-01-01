# import numpy as np
# import math
from decimal import Decimal
import random


def getKey(file):
    keys = open(file,"r").readlines()
    for key in keys:
        if '//' in key:
            pass
        else:
            data = key.split(',')
    X0 = Decimal(int(data[1])/int(data[2]))
    A = Decimal(data[0])
    return [A,X0,int(data[3]),float(data[4]),float(data[5])]

def generateKey():
    A=round(3.5+random.getrandbits(10)/1023*0.5,6)
    X0u = random.getrandbits(1024)
    X0d = random.getrandbits(1024)
    seed = random.getrandbits(8)
    while Decimal(X0u/X0d)>=1 or Decimal(X0u/X0d)==0:
        X0u = random.getrandbits(1024)
        X0d = random.getrandbits(1024)
    X0 = random.getrandbits(1024)/random.getrandbits(1024)
    Y0 = random.getrandbits(1024)/random.getrandbits(1024)
    key_file = open("key.txt","w")
    # key_file.write("{0:.f}".format(A))
    key_file.write("%f,%d,%d,%d,%f,%f"%(A,X0u,X0d,seed,X0,Y0))
    return [A, X0u, X0d, seed, X0, Y0]