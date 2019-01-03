import sys
import numpy as np 
from PIL import Image
import matplotlib.pyplot as plt


#for RGB type
def pixel_analysis(imageFile,name):
    Im = Image.open(imageFile,"r")

    print("target image mode : %s" %(Im.mode))
    pix = np.array(Im).astype('uint8')
    pix = pix.tolist()
    if Im.mode == "RGB" or Im.mode == "RGBA":
        print('ok')
        R=[]
        G=[]
        B=[]
        for i in range(0,len(pix)):
            for j in range(0,len(pix[i])):
                R.append(pix[i][j][0])
                G.append(pix[i][j][1])
                B.append(pix[i][j][2])
        plt.subplot(2,2,1)
        plt.title('picture')
        plt.imshow(Im)  
        plt.subplot(2,2,2)
        plt.title('pix(R)')
        plt.hist(R,bins=256,color='red')
        plt.subplot(2,2,3)
        plt.title('pix(G)')
        plt.hist(G,bins=256,color='green')
        plt.subplot(2,2,4)
        plt.title('pix(B)')
        plt.hist(B,bins=256,color='blue')
        # print(R)
        plt.tight_layout()
        plt.savefig("%s_analysis.png"%(name))

if __name__=="__main__":
        tname = sys.argv[1]
        dname = sys.argv[2]
        pixel_analysis(tname,dname)
