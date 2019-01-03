from PIL import Image
from decimal import Decimal
import sys, argparse, time
import numpy as np
from numpy import newaxis
from key_process import *
from mapping import *

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
    print("target image mode : %s" %(Im.mode))
    return pix, Im.mode

def diffusion(image_array, key: list):  # key = [A, X0, seed]
    en_image=[]
    # print(key)
    length = len(image_array)*len(image_array[0])*len(image_array[0][0])
    transient = 10000
    key_chaos = logistic_map(length+transient,key[0],key[1])[transient:]
    key_lfsr = LFSR(key[2], length)
    key = XOR(key_chaos,key_lfsr)
    # print(key)
    image_list = image_array.tolist()
    key = np.array(key)
    shape = ( len(image_list), len(image_list[0]),len(image_list[0][0]) )
    key = key.reshape(shape)
    # print(key)
    for row in range(0,len(image_list)):
        row_element=[]
        for pix in range(0,len(image_list[0])):
            pixel_element = XOR(image_list[row][pix],key[row][pix])
            row_element.append(pixel_element)
        en_image.append(row_element)
    en_image = np.array(en_image).astype('uint8')
    return en_image

def pixel_chaotic_shuffle(image_array, IC :list):
    image_list = image_array.tolist()
    #rearrange row elements
    #then rearrange whole row
    transient = 10000
    if len(image_list) > len(image_list[0]):
        max_len = len(image_list)
    else :
        max_len = len(image_list[0])  #choose bigger!!!!!!
    shift_key = np.array(Henon(max_len+transient,IC,1.4,0.3))[transient:]
    order_shift_key_X = shift_key[0:len(image_list[0]),0].argsort()
    rank_shift_key_X = order_shift_key_X.argsort()
    order_shift_key_Y = shift_key[0:len(image_list),1].argsort()
    rank_shift_key_Y = order_shift_key_Y.argsort()  
    # sort results are 
    #   small --> big  ( 0 --> max )
    tmp = []
    en_image = np.zeros((len(image_array),len(image_array[0]),len(image_array[0][0]))).astype('uint8')
    for i in range(0,len(image_list)):
        tmp.append(image_array[rank_shift_key_Y[i]])
    tmp = np.array(tmp)
    
    for i in range(0,len(image_list)):
        for j in range(0,len(image_list[0])):
            en_image[i,j] = tmp[i][rank_shift_key_X[j]]
    return en_image

def pixel_rearrangment(image_array, IC: list):
    image_list = image_array.tolist()
    transient = 10000
    if len(image_list) > len(image_list[0]):
        max_len = len(image_list)
    else :
        max_len = len(image_list[0])  #choose bigger!!!!!!
    shift_key = np.array(Henon(max_len+transient,IC,1.4,0.3))[transient:]
    order_shift_key_X = shift_key[0:len(image_list[0]),0].argsort()
    order_shift_key_Y = shift_key[0:len(image_list),1].argsort()
    tmp = np.zeros((len(image_array),len(image_array[0]),len(image_array[0][0]))).astype('uint8')
    for i in range(0,len(image_list)):
        for j in range(0,len(image_list[0])):
            tmp[i,j] = image_array[i][order_shift_key_X[j]]
    de_image = []
    for i in range(0,len(image_list)):
        de_image.append(tmp[order_shift_key_Y[i]])
    de_image = np.array(de_image)
    return de_image

def encrypt(target_file,key:list):
    rawData, mode = loadimage(target_file)
    # de_image_array, key = diffusion(en_image_array,key)
    shuffled_array = pixel_chaotic_shuffle(rawData, key[3:5])
    en_image_array = diffusion(shuffled_array,key)
    # en_image_array = shuffled_array
    encode_image = Image.fromarray(en_image_array,mode=mode)
    target_file = target_file.split('.')[0].split('/')[1]
    encode_image.save("image/%s_encoded.png"%(target_file),"PNG")
    print("successfully encrypted")

def decrypt(target_file, key:list):
    rawData, mode = loadimage(target_file)
    shuffled_array = diffusion(rawData,key)
    de_image_array = pixel_rearrangment(shuffled_array, key[3:5])
    decode_image = Image.fromarray(de_image_array,mode=mode)
    target_file = target_file.split('.')[0].split('/')[1]
    decode_image.save("image/%s_decoded.png"%(target_file),"PNG")
    print("successfully decrypted")


if __name__=="__main__":

    parser = argparse.ArgumentParser(description="script for image encryption")
    parser.add_argument('-e', '--encrypt', nargs='?')
    parser.add_argument('-d', '--decrypt', nargs='?')
    parser.add_argument('-k', '--key', nargs='?',default="key.txt")
    parser.add_argument('-g', '--generate_key',action='store_true')
    arguments = vars(parser.parse_args())
    if parser.parse_args().generate_key ==True:
        generateKey()
    
    key_file = arguments['key']

    # print(arguments)
    if arguments['encrypt'] != None :
        en_target_file = arguments['encrypt']    
        encrypt(en_target_file, getKey(key_file))
    if arguments['decrypt'] != None :
        de_target_file = arguments['decrypt']
        decrypt(de_target_file, getKey(key_file))
 
    