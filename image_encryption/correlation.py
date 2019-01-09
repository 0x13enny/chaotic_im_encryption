import numpy as np
import math, sys
import matplotlib.pyplot as plt
import pic_encryption

def correlation(image_array):
    image_array = image_array.astype('int')
    R1 = []
    R2 = []
    RGB=1
    # X = image_array[:,100,0]
    # Y = image_array[:,101,0]
    # X=[1,2,3,4,5,15,35,4,6,7,8,2,4,6,7,8,235,57,8,6]
    # Y=[9,8,2,2,3,56,27,67,56,563,536,7,8,9,54,23,2,456,8,2]
    for i in range(0,len(image_array[:,0,0])-1):
        X = image_array[i,:,RGB]
        Y = image_array[i+1,:,RGB]
        if len(X)==len(Y):
            n=len(X)
        else:
            raise IndexError
        sum_x=0
        sum_y=0
        sum_x_square=0
        sum_y_square=0
        sum_xy=0
        for  x,y in zip(X,Y):
            sum_x = sum_x + x
            sum_y = sum_y + y
            sum_x_square = sum_x_square + pow(x,2)
            sum_y_square = sum_y_square + pow(y,2)
            sum_xy = sum_xy + (x*y)
        r=abs((n*sum_xy-sum_x*sum_y)/\
            math.sqrt((n*sum_x_square-pow(sum_x,2))*(n*sum_y_square-pow(sum_y,2))))    
        R1.append(r)
    for i in range(0,len(image_array[0,:,0])-1):
        X = image_array[:,i,RGB]
        Y = image_array[:,i+1,RGB]
        if len(X)==len(Y):
            n=len(X)
        else:
            raise IndexError
        sum_x=0
        sum_y=0
        sum_x_square=0
        sum_y_square=0
        sum_xy=0
        for  x,y in zip(X,Y):
            sum_x = sum_x + x
            sum_y = sum_y + y
            sum_x_square = sum_x_square + pow(x,2)
            sum_y_square = sum_y_square + pow(y,2)
            sum_xy = sum_xy + (x*y)
        r=abs((n*sum_xy-sum_x*sum_y)/\
            math.sqrt((n*sum_x_square-pow(sum_x,2))*(n*sum_y_square-pow(sum_y,2))))    
        R2.append(r)
    plt.subplot(2,1,1)
    plt.title('rows correlation')
    plt.axis(xmin=0,xmax=len(R1),ymin=0,ymax=1)
    plt.plot(R1) #data_row 
    plt.subplot(2,1,2)
    plt.title('columns correlation')
    plt.axis(xmin=0,xmax=len(R2),ymin=0,ymax=1)
    plt.plot(R2) #data_column
    plt.tight_layout() 
    plt.savefig('analysis/correlation.png')

    return R1, R2

def NPCR_UACI(origin_array, encrypted_array):
    N=0
    C=0
    T=0
    L=len(origin_array[0,0])
    for origin_row , encrypted_row in zip(origin_array,encrypted_array):
        for origin_pix, encrypted_pix in zip(origin_row,encrypted_row):
            tmp = 0
            for element in abs(origin_pix-encrypted_pix):
                tmp += element
            tmp /= (225*L)
            N += 1
            T += tmp
            if (origin_pix==encrypted_pix).all():
                C += 1
    pix_change_rate = 1 - C/N
    changing_intensity = T/N
    return pix_change_rate, changing_intensity

def return_map(origin_array,encrypted_array):
    R_origin_x=[]
    R_origin_y=[]
    R_encrypted_x=[]
    R_encrypted_y=[]
    for i in range(0,len(origin_array)-1):
        for j in range(0,len(origin_array[0,:])-2):            
            R_origin_x.append(origin_array[i,j,0])
            R_origin_y.append(origin_array[i,j+1,0])          
            R_encrypted_x.append(encrypted_array[i,j,0])
            R_encrypted_y.append(encrypted_array[i,j+1,0])
    plt.subplot(1,2,1)
    plt.scatter(R_origin_x,R_origin_y,s=1)
    plt.subplot(1,2,2)
    plt.scatter(R_encrypted_x,R_encrypted_y,s=1)
    plt.savefig('analysis/return_map')
if __name__ == "__main__":
    target=sys.argv[1]
    en_target=sys.argv[2]
    image_array, mode = pic_encryption.loadimage(target)
    en_image_array, mode = pic_encryption.loadimage(en_target)
    # return_map(image_array,en_image_array)
    # data_row,data_column  = correlation(image_array)
    # data_row,data_column = correlation(en_image_array)
    print(NPCR_UACI(image_array,en_image_array))