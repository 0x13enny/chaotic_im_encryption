import numpy as np
# import math
from decimal import * 
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
    return [A,X0,int(data[3])]

def generateKey():
    A=round(3.5+random.getrandbits(10)/1023*0.5,6)
    X0u = random.getrandbits(1024)
    X0d = random.getrandbits(1024)
    seed = random.getrandbits(8)
    while Decimal(X0u/X0d)>=1 or Decimal(X0u/X0d)==0:
        X0u = random.getrandbits(1024)
        X0d = random.getrandbits(1024)
    key_file = open("key.txt","w")
    # key_file.write("{0:.f}".format(A))
    key_file.write("%f,%d,%d,%d"%(A,X0u,X0d,seed))
    return [A,X0u,X0d,seed]
    
if __name__=="__main__":
    # print(math.pow(2,1023)-89*math.pow(10,306)) #maximum 
    # X0 = math.pow(2,-50) + 0.15  #is able to detect two different in 50 map    
    # X0 = math.pow(2,-1000) + 0.15  #cannot detect two different even 500000 map
    X0 = 0.15
    # X0 = math.pow(2,-70) + 0.15  #cannot detect two different even 500000 map