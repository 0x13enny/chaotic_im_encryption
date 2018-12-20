from PIL import Image
import sys, argparse
import numpy as np

def chaotic_map(series_len,a,X0):
#   logistic map
#   X[n+1]=A*X[n](1-X[n])
    X = [X0]
    for i in range(0,series_len-1):

        tmp = logistic(X[-1],a)
        X[-1] = int(round(X[-1]*255,0))
        # if tmp in X:
        #     print("periodic detection : %s" %(len(X)))
        #     sys.exit(1)
        X.append(tmp)
    X[-1] = int(round(X[-1]*255,0))    
    return X

def logistic(Xn,a):
    Xn1=a*Xn*(1-Xn)
    return Xn1

def LFSR(seed: int,len):
    key = []
    bit8 = seed
    for i in range(0,len):
        bit8str = '{0:08b}'.format(bit8)
        if int(bit8str[0])==int(bit8str[4])==int(bit8str[5])==int(bit8str[6]):
            newbit = 1
        else:
            newbit = 0
        bit8 = ((bit8<<1) + newbit)%256
        key.append(bit8)
    return key
def XOR(A,B):
    P = []
    for i in A:
        j = B[A.index(i)]
        P.append(i^j)
    return P

def loadimage(file):
    Im = Image.open(file, "r")
    pix = np.array(Im)
    return pix

def encryption(image_array, params: list):  # params = [A, X0, seed]
    en_image=[]
    length = len(image_array)*len(image_array[0])*len(image_array[0][0])
    # efficiency warning
    key_chaos = chaotic_map(length,params[0],params[1])
    # print(key_chaos)
    key_lfsr = LFSR(params[2], length)
    # print(key_lfsr)
    key = XOR(key_chaos,key_lfsr)
    # print(key)
    print(image_array)
    image_array = image_array.tolist()
    for h in image_array:
        row_element=[]
        for w in h:
            pixel_element=[]
            row_index = image_array.index(h)
            pixel_index = h.index(w)
            # (w+1)*(h+1)
            index = (row_index+1)*(pixel_index+1)*3
            pixel_element = XOR(w,key[index-3:index])
            row_element.append(pixel_element)
        en_image.append(row_element)
    en_image = np.array(en_image)
    return en_image, key

def decription():
    pass

if __name__=="__main__":
    params=[4, 0.5111, 25]
    
    en_image_array, key = encryption(loadimage("image/test.jpg"),params)
    de_image_array, key = encryption(en_image_array,params)


    # print("en",en_image_array)
    # print("de",de_image_array)

    # P = Image.new('RGB',(512,256))
    newImg1 = Image.fromarray(en_image_array,"RGB")
    newImg1.save("encoded.png","PNG")
    # print(np.array(Image.open("encoded.png",'r')))
    newImg2 = Image.fromarray(de_image_array,"RGB")
    newImg2.save("decoded.png","PNG")
    # print(np.array(Image.open("decoded.png",'r')))