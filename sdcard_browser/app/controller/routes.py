# from sdcard_metadata_22a import *
from .camera_client import Camera
from .plotter import *
from .collector import *
from .events import *
# from .thumbnail import *
from flask import render_template, request, redirect , url_for, Response
from . import blueprint
import threading,time
from .. import socketio

@blueprint.route('/', methods=['GET','POST'])
def sd_browser_home(err=''):

    if request.method=='POST':
        err=''
        if request.form['send']=='send':
            jumboId=str(request.form['camid']).upper()
            return redirect('/%s'%(jumboId))
    else:
        return render_template("home.html",err_msgs=err)


@blueprint.route('/<jumboId>',methods=['GET'])
def in_camera(jumboId):
    Cam = Camera(jumboId)
    Cam.create_ssh_client()
    if Cam.status =="Online":
        Cam.get_dir_structure()
        sd_info = get_sd_info(Cam)
        videos_data_process = collect_video_data(Cam)
        # dataplot
    else:
        err='%s unreachable'%(jumboId)
        return redirect(url_for('.sd_browser_home', err=err))
    dates=[]
    for key in Cam.dir_structure:
        dates.append(key)
    bgthreads=[]

    # bgthreads.append(socketio.start_background_task(target=write_sd_card_Cam.create_ssh_client()files,args=(Cam,Cam.dir_structure),indicater=0,name='sdFile'))
    # bgthreads.append(socketio.start_background_task(target=videos_data_process.write_videos_info,specified_date=20181113,name='videoData')) #kwargs='<dates>'to improve efficiency
    bgthreads.append(threading.Thread(target=write_sd_card_files,\
            args=(Cam,Cam.dir_structure),kwargs={'indicater':0},name='sdFile'))
    bgthreads.append(threading.Thread(target=videos_data_process.write_videos_info,\
            kwargs={'specified_date':'20181113'},name='videoData'))
    for thread in bgthreads:
        thread.start()
    return render_template("in_camera.html",sd_info=sd_info,jumboId=jumboId,time_infos=dates)

@blueprint.route('/<jumboId>',methods=["POST"])
def go_thumbnails(jumboId):
    if 'dates' in request.form:
        date = str(request.form['dates'])
        return redirect('/%s/%s' %(jumboId,date))

    elif 'keep_csv' in request.form:
        pass

    elif 'keep_plots' in request.form:
        pass

@blueprint.route('/<jumboId>/<date>',methods=['GET'])
def display_some(jumboId,date):
    
    # default image
    return render_template('deep_in.html',date=date,jumboId=jumboId,filenames=[1,2,3,3,4,6,7])

@blueprint.route('/<jumboId>/<date>',methods=['POST'])
def download_some(jumboId,date):
    pass# switch to gif
        # switch