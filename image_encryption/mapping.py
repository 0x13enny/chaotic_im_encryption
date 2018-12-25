from decimal import Decimal
import math
import numpy as np

def logistic(Xn,a):
#   logistic map
#   X[n+1]=A*X[n](1-X[n])
    Xnp=a*Xn*(1-Xn)
    return Xnp

def Baker(initial: list):
    # Baker's map
    # for 0<= X < 0.5
        # (X[n+1],Y[n+1]) = (2*X[n],Y[n]/2)
    # for 0.5<= X < 1
    #     (X[n+1],Y[n+1]) = (2-2*X[n],1-Y[n]/2)
    if (initial[0] < 0.5) and (initial[0] >= 0):
        Xnp = 2*initial[0]
        Ynp = initial[1]/2.0
    elif (initial[0] < 1) and (initial[0] >= 0.5):
        Xnp = 2-2*initial[0]
        Ynp = 1-initial[1]/2.0
    else:
        raise ValueError
    return [Xnp,Ynp]

def Henon(initial: list,a,b):
    # Henon map
    # X[n+1]=1-a*(X[n]^2)+Y[n]
    # Y[n+1]=b*X[n]
    Xnp = 1 - a*(math.pow(initial[0],2)) + initial[1]
    Ynp = b*initial[0]
    return [Xnp,Ynp]

def Chirikov(initial: list,k):
    # Standard map
    # P[n+1] = P[n] + K*sin(T[n])
    # T[n+1] = T[n] + P[n+1]
    # T as theta in radius
    Pnp = initial[0] + k*(math.sin(initial[1]))
    Tnp = (initial[1] + Pnp)%(2*(math.pi))
    return [Pnp,Tnp]



if __name__=="__main__":
    IC = [2,0.3]
    for i in range(1,1000):
        IC = Chirikov(IC,0.6)
        # IC = Henon(IC,1.4,0.3)
        print(IC)