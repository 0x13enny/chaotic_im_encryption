
from controller.camera_client import Camera
from controller.calculater import collect_video_data
import argparse, time, threading
# import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--jumboId", type=str,help="target camera",metavar='',required=True)
parser.add_argument("-d", "--date", type=str,default=time.strftime("%Y%m%d",time.localtime()),help="specify date to save loading time form : YYYYMMDD",metavar='')
args = parser.parse_args()

def test_entry(jumboId,specified_date):
    
    #setup client
    Cam = Camera(jumboId)
    status = Cam.create_ssh_client()
    dir_structure = Cam.get_dir_structure()
    videos_data_process = collect_video_data(Cam)


    # sd_data = write_sd_card_files(Cam,dir_structure,specified_date,indicater=0)
    video_data = videos_data_process.write_videos_info(specified_date=specified_date)
    Cam.exit()


if __name__=="__main__":

    test_entry(args.jumboId,args.date) #id-12345678 , YYYYMMDD