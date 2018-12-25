from PIL import Image
from decimal import Decimal
import sys, argparse, time
import numpy as np
from key_process import *
from mapping import *

def chaotic_map(series_len,a,X0):
    X = [X0]
    for i in range(0,series_len-1):
        # print(X[-1])
        tmp = logistic(X[-1],a)
        X[-1] = int(round(X[-1]*255,0))
        # if tmp in X:
        #     print("periodic detection : %s" %(len(X)))
        #     sys.exit(1)
        X.append(tmp)
    X[-1] = int(round(X[-1]*255,0))    
    return X

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
    pix = np.array(Im).astype('uint8')
    return pix, Im.mode

def diffusion(image_array, params: list):  # params = [A, X0, seed]
    en_image=[]
    length = len(image_array)*len(image_array[0])*len(image_array[0][0])
    
    key_chaos = chaotic_map(length,params[0],params[1])
    key_lfsr = LFSR(params[2], length)
    key = XOR(key_chaos,key_lfsr)
    # print(key)
    image_array = image_array.tolist()
    key = np.array(key)
    shape = ( len(image_array), len(image_array[0]),len(image_array[0][0]) )
    key = key.reshape(shape)
    # print(key)
    # print(image_array)
    for row in range(0,len(image_array)):
        row_element=[]
        for pix in range(0,len(image_array[0])):

            pixel_element = XOR(image_array[row][pix],key[row][pix])
            row_element.append(pixel_element)
        en_image.append(row_element)
    en_image = np.array(en_image).astype('uint8')
    return en_image, key

def pixel_chaotic_shuffle():
    pass

def test(file,params):

    rawData, mode = loadimage(file)
    # print(rawData)
    en_image_array, key = diffusion(rawData,params)
    de_image_array, key = diffusion(en_image_array,params)
    # print(en_image_array)
    # print(de_image_array)
    encode_image = Image.fromarray(en_image_array,mode=mode)
    encode_image.save("image/encoded.png","PNG")


if __name__=="__main__":

    parser = argparse.ArgumentParser(description="script for image encryption")
    parser.add_argument('-t', '--target', nargs='?', required=True)
    parser.add_argument('-k', '--key', nargs='?',default="key.txt")
    parser.add_argument('-g', '--generate_key',action='store_true')
    arguments = vars(parser.parse_args())
    if parser.parse_args().generate_key ==True:
        print(generateKey())

    
    # target_file = arguments['target']
    # key_file = arguments['key']
    # test(target_file,getKey(key_file))
    print("encryption success")
 
    