import numpy as np
import math
from decimal import Decimal #55 digits

def getKey(file):
    keys = open(file,"r").readlines()
    for key in keys:
        if '//' in key:
            pass
        else:
            data = key.split(',')
    X0 = Decimal(int(data[1])/int(data[2]))
    return [int(data[0]),X0,int(data[3])]

    
if __name__=="__main__":
    # print(math.pow(2,1023)-89*math.pow(10,306)) #maximum 
    # print(converKey())


    # X0 = 0.15
    # X0 = math.pow(2,-50) + 0.15  #is able to detect two different in 50 map
    

    # X0 = 0.15
    # X0 = math.pow(2,-1000) + 0.15  #cannot detect two different even 500000 map
    
    X0 = 0.15
    # X0 = math.pow(2,-70) + 0.15  #cannot detect two different even 500000 map
    
    
    # print(chaotic_map(50000,4,X0))