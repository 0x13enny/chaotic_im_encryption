from decimal import Decimal
import math
import numpy as np

    
def logistic_map(series_len,a,X0):
#   logistic map
#   X[n+1]=A*X[n](1-X[n])
    X = [X0]
    for i in range(0,series_len-1):
        # print(X[-1])
        tmp=a*X[-1]*(1-X[-1])
        X[-1] = int(round(X[-1]*255,0))
        # if tmp in X:
        #     print("periodic detection : %s" %(len(X)))
        #     sys.exit(1)
        X.append(tmp)
    X[-1] = int(round(X[-1]*255,0))    
    return X

def Baker(IC: list):
    # Baker's map
    # for 0<= X < 0.5
        # (X[n+1],Y[n+1]) = (2*X[n],Y[n]/2)
    # for 0.5<= X < 1
    #     (X[n+1],Y[n+1]) = (2-2*X[n],1-Y[n]/2)
    if (IC[0] < 0.5) and (IC[0] >= 0):
        Xnp = 2*IC[0]
        Ynp = IC[1]/2.0
    elif (IC[0] < 1) and (IC[0] >= 0.5):
        Xnp = 2-2*IC[0]
        Ynp = 1-IC[1]/2.0
    else:
        raise ValueError
    return [Xnp,Ynp]

def Henon(series_len, IC: list,a,b):
    # Henon map
    # X[n+1]=1-a*(X[n]^2)+Y[n]
    # Y[n+1]=b*X[n]
    XY = [IC]
    for i in range(0,series_len-1):
        # print(XY)
        Xnp = 1 - a*(math.pow(XY[-1][0],2)) + XY[-1][1]
        Ynp = b*XY[-1][0]
        XY.append([Xnp,Ynp])
    return XY

def Chirikov(series_len,IC: list,k):
    # Standard map
    # P[n+1] = P[n] + K*sin(T[n])
    # T[n+1] = T[n] + P[n+1]
    # T as theta in radius
    Pnp = IC[0] + k*(math.sin(IC[1]))
    Tnp = (IC[1] + Pnp)%(2*(math.pi))
    return [Pnp,Tnp]



if __name__=="__main__":
    IC = [0.5,0.3]
    print(Henon(1000,IC,1.4,0.3))
    # print(IC)