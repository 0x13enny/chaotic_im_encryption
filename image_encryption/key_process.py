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
    return [int(data[0]),X0,int(data[3])]

    
def generateKey():
    A=3.5+random.getrandbits(10)/1023*0.5
    X0u = random.getrandbits(1024)
    X0d = random.getrandbits(1024)
    seed = random.getrandbits(8)
    while Decimal(X0u/X0d)>=1 or Decimal(X0u/X0d)==0:
        X0u = random.getrandbits(1024)
        X0d = random.getrandbits(1024)
    
    return [A,X0u,X0d,seed]
if __name__=="__main__":
    # print(math.pow(2,1023)-89*math.pow(10,306)) #maximum 
    # print(converKey())
    # print(generateKey())
    # X0 = 0.15
    # X0 = math.pow(2,-50) + 0.15  #is able to detect two different in 50 map
    

    # X0 = 0.15
    # X0 = math.pow(2,-1000) + 0.15  #cannot detect two different even 500000 map
    
    X0 = 0.15
    # X0 = math.pow(2,-70) + 0.15  #cannot detect two different even 500000 map
    
    
    # print(chaotic_map(50000,4,X0))