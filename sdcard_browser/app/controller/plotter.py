import matplotlib.pyplot as plt
from matplotlib import dates
import time, os
from . import events
import pandas as pd
import numpy as np
from flask_socketio import emit
from .. import app, socketio
import datetime

def plot_file_size(jumboId,mode): #working   #ave_fps, sd card, 

    df = pd.read_csv('app/static/csv_generated/%s/%s.csv'%(jumboId,mode))
    newData={}
    accumulation = 0
    time_series=[]
    plt.clf()
    
    plt.figure(1)
    plt.style.use('dark_background')
    # ax1 = plt.subplots(1,2,1)
    # ax2 = plt.subplots(1,2,2)

    datelist = df['time'].tolist()
    filelist = df[mode].tolist()
    # min_x = int(time.mktime(datetime.datetime.strptime(datelist[0][0:13],'%Y-%m-%d:%H').timetuple()))
    # max_x = int(time.mktime(datetime.datetime.strptime(datelist[-1][0:13],'%Y-%m-%d:%H').timetuple()))

    fig, ax = plt.subplots(2,1)
    fig.patch.set_facecolor("none")
    accumulationList=[]
    accumulation=0
    for index, row in df.iterrows():
        try:
            accumulation += row[mode]
            accumulationList.append(accumulation)
        except ValueError:
            pass
    ylabel='dataSize(Mb)'
    xlabel='time'
    ax[0].set_title('Instance File Size')
    ax[1].set_title('Accumulation')
    
    ax[0].scatter(datelist,filelist,c='white',s=4)
    ax[1].scatter(datelist, accumulationList, c='white', s=4)
    for plot in ax:
        plot.set_facecolor((0.356, 0.376, 0.403))
        for tick in plot.xaxis.get_ticklines():
            if plot.xaxis.get_ticklines().index(tick)%16!=0:
                tick.set_visible(False)
        for label in plot.xaxis.get_ticklabels():
            if plot.xaxis.get_ticklabels().index(label)%8!=0:
                label.set_visible(False)
        plot.set_xticklabels(datelist, rotation=20, horizontalalignment = 'right')
        plot.set_ylabel(ylabel)
        plot.set_xlabel(xlabel)

    plt.tight_layout()
    filename='app/static/image_generated/%s/%s.png'%(jumboId,mode)
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    plt.savefig(filename, facecolor=fig.get_facecolor(), edgecolor='none')

    time.sleep(10)
    print('%s/%s.png ready'%(jumboId,mode))
    # ================================
    
    with app.test_request_context('/'+jumboId):
        events.send_message('%s/%s.png'%(jumboId,mode),jumboId)
    # =======================
    # with app.test_request_context('/'):
    #     print('%s/%s.png ready'%(jumboId,mode))
    #     socketio.emit('sdFigReady','%s/%s.png'%(jumboId,mode),broadcast=True)
    
def plot_ffmpeg_info(jumboId,specified_date): #kpbs fps
    df = pd.read_csv('app/static/csv_generated/%s/videos_%s.csv'%(jumboId,specified_date))
    plt.clf()
    plt.figure(2)
    plt.style.use('dark_background')
    fig, ax = plt.subplots(nrows=1, ncols=1)
    fig.patch.set_facecolor("none")
    ax.set_facecolor((0.356, 0.376, 0.403))
    datelist = df['timeStamp'].tolist()
    kbps = df['ave_kbps'].tolist()
    fps = df['ave_fps'].tolist()
    time = df['time'].tolist()
    plt.scatter(datelist,kbps,c='red',s=4)
    plt.scatter(datelist,fps,c='orange',s=4)
    plt.scatter(datelist,time,c='green',s=4)
    for tick in ax.xaxis.get_ticklines():
            if ax.xaxis.get_ticklines().index(tick)%16!=0:
                tick.set_visible(False)
    for label in ax.xaxis.get_ticklabels():
            if ax.xaxis.get_ticklabels().index(label)%8!=0:
                label.set_visible(False)
    ax.set_xticklabels(datelist, rotation=20, horizontalalignment = 'right')
    ax.set_xlabel('time')
    plt.legend(['ave_bandwidth(kpbs)','ave_fps','time(s)'])
    plt.title('videos_info')
    filename='app/static/image_generated/%s/videos_%s.png'%(jumboId,specified_date)
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    plt.savefig(filename, facecolor=fig.get_facecolor(), edgecolor='none')
    print('%s/videos_%s.png ready'%(jumboId,specified_date))
    # ==================
    with app.test_request_context('/'+jumboId):
        socketio.emit('vidFigReady','%s/videos_%s.png'%(jumboId,specified_date),namespace='/%s'%(jumboId))