
#the feature is working


import subprocess, sys, scp, time,threading
# from camera_client import Camera
from .camera_client import Camera
from .collector import *

def tnHunter():

    start = time.time()
    idleTime=0
    while idleTime<60:
        if targets==[]:
            pass
            # stdout = subprocess.getoutput('ls ../tmp/*.mp4').split('\n')
            # for result in stdout:
            #     if result.split('/')[-1] not in targets:
            #         targets.append(result.split('/')[-1])
        else:
            print('hunter activated')
            target=targets[-1]
            targets.remove(target)
            output=target.replace('.mp4','.png')
            subprocess.Popen('cd app/tmp; ffmpeg -loglevel panic -ss 1 -i %s -an -vframes 1 %s ;rm %s' %(target,output,target),shell=True) #ffmpeg tnnail&GIF
            print('hunter deactivated')
            start = time.time()
        idleTime=time.time()-start
def gifHunter():
    pass

def trafficMission(jumboId,date,hour):  #280secs for an hour videos
    
    Cam = Camera(jumboId)
    global targets
    targets=[]
    Cam.create_ssh_client()
    ffmpegWatchDogs=[]

    with scp.SCPClient(Cam.client.get_transport(),sanitize=lambda x: x) as cp:

        files = Cam.command('ls /mnt/sdcard/{}/{}'.format(date,hour))[0].split('\n')
        targetDir='/mnt/sdcard/{}/{}/'.format(date,hour)
        
        # for i in range(0,3):
        ffmpegWatchDogs.append(threading.Thread(target=tnHunter))
        ffmpegWatchDogs[-1].start()

        for targetFile in files:
            if targetFile!='':
                cp.get(targetDir+targetFile,'../tmp')
                targets.append(targetFile)

    # cp.get('/mnt/sdcard/2018-10-03/05/','')
if __name__ == "__main__":
    a=time.time()
    trafficMission()
    # tnHunter()
    print(time.time()-a)