
# H264 Main@4, 60.000 secs, 871 kbps, 1920x1080 @ 30.000000 fps'
import re,csv,time,datetime,sys,threading,os
import pandas as pd
from .camera_client import Camera
from .plotter import *


class collect_video_data():

    def __init__(self,Cam):
        self.Threads=[]
        self.Cam = Cam
        self.data = {}
        self.dir_structure = Cam.dir_structure

    def write_videos_info(self,specified_date=time.strftime("%Y%m%d",time.gmtime())):
        
        
        if specified_date=="all":
            for date in self.dir_structure:
                for hour in self.dir_structure[date]:
                    self.doc_chip_info(date,hour)
                    # self.Threads.append(threading.Thread(target=self.doc_chip_info,args=(date,hour)))
                    # self.Threads[-1].start()
                    # time.sleep(0.1)
        else:
            for date in self.dir_structure:
                if date.replace('-','')==specified_date:
                    for hour in self.dir_structure[date]:
                        self.doc_chip_info(date,hour)
                        # self.Threads.append(threading.Thread(target=self.doc_chip_info,args=(date,hour)))
                        # self.Threads[-1].start()
                        # time.sleep(0.1)
                else:
                    pass
        # for Thread in self.Threads:
        #     Thread.join()
        if self.data=={}:
            print("specified date doesn't exist")
            sys.exit(1)
        self.process_raw_video_data()
        self.conti_or_boost()
        # print(pd.DataFrame(data=self.data))
        filename = "app/static/csv_generated/%s/videos_%s.csv"%(self.Cam.jumboID,specified_date)
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename,'w',newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')

            writer.writerow(['timeStamp','time','ave_kbps','ave_fps','resolute','frame_mode','sd_rec_mode'])
                                        #,'time02','ave_kbps02','ave_fps02','resolute02','frame_mode02','sd_rec_mode02'])
            for key in self.data:
                if len(self.data[key][0])==6 and len(self.data[key][1])==6:
                    writer.writerow([key+'::00',self.data[key][0]['time'],self.data[key][0]['ave_kbps'],self.data[key][0]['ave_fps'],self.data[key][0]['resolute'],self.data[key][0]['frame_mode'],self.data[key][0]['sd_rec_mode']])
                    writer.writerow([key+'::30',self.data[key][1]['time'],self.data[key][1]['ave_kbps'],self.data[key][1]['ave_fps'],self.data[key][1]['resolute'],self.data[key][1]['frame_mode'],self.data[key][1]['sd_rec_mode']])
        
        plot_ffmpeg_info(self.Cam.jumboID,specified_date) #videos_%s.csv"%(specified_date)
        return self.data

    def doc_chip_info(self,date,hour):  #chip stand for 30 mins video  #take lots of time, need approving

        time_pat=re.compile("\d+\-\d{2}(?P<min>\d{2})")
        mp4info = self.Cam.command('mp4info /mnt/sdcard/{}/{}/*.mp4'.format(date,hour))[0].split('\n')
        video_info1={}
        video_info2={}
        for line in mp4info:
            if ".mp4:" in line:
                time = line.split('/')[-1]
            if line.split('\t')[0]=='1':
                if int(time_pat.search(time).group("min"))<30:
                    video_info1.update({time : line.split('\t')[2]}) #0-29
                else:
                    video_info2.update({time : line.split('\t')[2]})  #30-59
            else:
                pass
        self.data.update({"{}:{}".format(date,hour):[video_info1,video_info2]})

    def process_raw_video_data(self): #data is a huge dictionary 
        Pat = re.compile("@\d+,\s+(?P<time>\d+\.\d+)\s+\w+,\s+(?P<kbps>\d+)\s+\w+,\s+(?P<resolute>.+)\s+@\s+(?P<fps>\d+.\d+)")
        #{hour:[{ave_infos1},{ave_infos2}]
        
        for hour_key in self.data:
            for half_hour_dic in self.data[hour_key]:
                count=0
                half_hour={"time":0.0 ,'ave_kbps':0.0 ,'ave_fps':0.0,'resolute':[0,0],'frame_mode':'higher_image_quality'} 
                for time_key in half_hour_dic:
                    R = Pat.search(half_hour_dic[time_key])
                    if R == None:
                        pass
                    else:
                        half_hour['time']+=float(R.group('time'))
                        half_hour['ave_kbps']+=float(R.group('kbps'))
                        half_hour['ave_fps']+=float(R.group('fps'))
                        if float(R.group('fps'))>25:
                            half_hour['frame_mode']='higher_frame_rate'
                        if "1920x1080" in R.group('resolute'):
                            half_hour['resolute'][1]+=1
                        elif "1280x720" in R.group('resolute'):
                            half_hour['resolute'][0]+=1
                        count+=1
                if count>=1:
                    half_hour['time']= round(half_hour['time']/count,2)
                    half_hour['ave_kbps']=round(half_hour['ave_kbps']/count,2)
                    half_hour['ave_fps']=round(half_hour['ave_fps']/count,2)
                    index = self.data[hour_key].index(half_hour_dic)
                    self.data[hour_key][index] = half_hour
                else:
                    pass

    def conti_or_boost(self):
        config = self.Cam.command('cat {}'.format(self.Cam.camera_config))[0].split('\n\n')
        weekday_config={}
        for line in config:
            if "[Recording]" in line: 
                for day in line.split('\n'):
                    if 'monday' in day:
                        weekday_config.update({1:day.split('=')[-1]})
                    elif 'tuesday' in day:
                        weekday_config.update({2:day.split('=')[-1]})
                    elif 'wednesday' in day:
                        weekday_config.update({3:day.split('=')[-1]})
                    elif 'thursday' in day:
                        weekday_config.update({4:day.split('=')[-1]})
                    elif 'friday' in day:
                        weekday_config.update({5:day.split('=')[-1]})
                    elif 'saturday' in day:
                        weekday_config.update({6:day.split('=')[-1]})
                    elif 'sunday' in day:
                        weekday_config.update({7:day.split('=')[-1]})
        for key in self.data:
            date_info = key.split(':')[0].split('-')  #date
            hour_info = int(key.split(':')[-1])
            try:
                weekday = datetime.date(int(date_info[0]),int(date_info[1]),int(date_info[2])).isoweekday()
            except ValueError:
                weekday = None
            if weekday!=None:
                conti = weekday_config[weekday][hour_info]
                if conti == "A":
                    conti = 10
                conti = int(conti)
                front_half = int(conti / 4)
                back_half = (conti % 4)
                for chip in self.data[key]:
                    if self.data[key].index(chip)==0:
                        half_hour = front_half
                    else:
                        half_hour = back_half
                    if half_hour ==0:
                        chip.update({'sd_rec_mode':'no sd Recording'})
                    elif half_hour==1:
                        chip.update({'sd_rec_mode':'boost recording'})
                    elif half_hour==2:
                        chip.update({'sd_rec_mode':'continuous recording'})
            

def write_sd_card_files(Cam,dir_struct,specified_date=time.strftime("%Y%m%d",time.gmtime()),specified_hour=time.strftime("%H",time.gmtime()),indicater=0): 
    #indicater 0 = whole sd  1 = 1 day  2 = 1 hour
    
    if indicater==1:
        mode='{}(halfHourly)'.format(specified_date)
        mp4_size={'time':mode}
        for date in dir_struct:
            if date.replace('-','')==specified_date:
                raws = Cam.command('du /mnt/sdcard/{}/*/*.mp4'.format(date))[0].split('\n') #du -hs path
                size1=0
                size2=0
                time=''
                del raws[raws.index("")]
                for raw in raws:
                    if ((raw.split('/')[-1].split('-')[-1][0:2])!=time) and raws.index(raw)!=0:
                        mp4_size.update({ "{}:{}::00|29".format(date,time):round(size1,2) }) #ex:22::00|29
                        mp4_size.update({ "{}:{}::30|59".format(date,time):round(size2,2) })
                        size1=0
                        size2=0
                    minute = raw.split('/')[-1].split('-')[-1][2:4]
                    if int(minute)>=30.0:
                        size2 = float(raw.split('\t')[0])/1024.0 + size2 #in Mb
                        time = raw.split('/')[-1].split('-')[-1][0:2]
                    else:
                        size1 = float(raw.split('\t')[0])/1024.0 + size1 #in Mb
                        time = raw.split('/')[-1].split('-')[-1][0:2]
                    if raws[-1]==raw:
                        mp4_size.update({ "{}:{}::00|29".format(date,time):round(size1,2) }) 
                        mp4_size.update({ "{}:{}::30|59".format(date,time):round(size2,2) })
    elif indicater==0:
        mode='overall(hourly)'
        mp4_size={'time':mode}
        for date in dir_struct:
            raws = Cam.command('du /mnt/sdcard/{}/*/'.format(date))[0].split('\n')
            del raws[raws.index("")]
            for raw in raws:
                size = float(raw.split('\t')[0])/1024.0
                time = raw.split('/')[-2]
                mp4_size.update({ "{}:{}::00".format(date,time):round(size,2) })
                
    elif indicater==2:
        mode='{}_{}(minutely)'.format(specified_date,specified_hour)
        mp4_size={'time':mode}
        for date in dir_struct:
            if date.replace('-','')==specified_date:
                for hour in dir_struct[date]:
                    if int(hour) == int(specified_hour):
                        raws = Cam.command('du /mnt/sdcard/{}/{}/*.mp4'.format(date,hour))[0].split('\n') #du -hs path
                        del raws[raws.index("")]
                        for raw in raws:
                            time = raw.split('/')[-1].split('-')[-1][2:4]
                            size = round(float(raw.split('\t')[0])/1024.0,2)
                            mp4_size.update({"{}:{}::{}".format(date,hour,time):size })

    filename="app/static/csv_generated/{}/{}.csv".format(Cam.jumboID,mode)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename,'w',newline='') as csvfile:
        writer = csv.writer(csvfile,delimiter=',')
        for key in mp4_size:
            writer.writerow([key,mp4_size[key]])
    plot_file_size(Cam.jumboID,mode)
    return mp4_size

def get_sd_info(Cam):
    sd_info = Cam.command('df -h /mnt/sdcard/')[0].split('\n')[1].replace(' ','\n').split('\n')
    sd_info = list(filter(None,sd_info))
    # print(sd_info)
    return [sd_info[3],sd_info[2],sd_info[1]]