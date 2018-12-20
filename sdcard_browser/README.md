# SD Card Browser Web Server

## Description
For all the tests involving SD Card Recording, it's inconvenient to check videos profile by download it. This project is to solve the invonvenience by running a web server. Whoever visits the web can browse the sd card information (including video properties, disk usage messages, or even thumbnail and gif) in the camera (now It's only for DomePlus and Bullet) in local network by jumboId.


## Prerequisites
The server run on python3 

### Environment variables
```
export CAMUSERID=<userid>
export CAMPASSWORD=<cam_password>
export CONFIG_INI=<path_to_config_ini>
```

### Requirement
It's recommand to create a conda environment to manage the packages

```
conda -n <your_conda_environment_name> install argparse \
ffmpeg \
paramiko \
subprocess \
matlibplot \
scp \
eventlet \
flask \
flask_socketio
```

or simply
```
pip3 install argparse \
ffmpeg \
paramiko \
subprocess \
matlibplot \
scp \
eventlet \
flask \
flask_socketio
```

## Usage 

activate the server
```
python3 entry.py
```

Ctrl+C to deactivate the server



## Notes

files structure
```
+-- challange22
    +--entry.py
    +--app/
        +--__init__.py
        +--sdcard_metadata_22a.py
        +--controller/
            +--__init__.py
            +--camera_client.py
            +--collertor.py
            +--events.py
            +--plotter.py
            +--routes.py
            +--thumb_generater.py
        +--static/
            +--css/
                ...
            +--csv_generated/
            +--image_generated/
            +--image_src/
        +--templates/
            ...
        +--tmp/
        
    +--README.md
```

## Issue
- - - - 
### socket server cannot actively raise an event to client 
when client jumboId is filled and send, the server will spawn two threads to collect sdcard info and write them to csv. But the works need some time, so I hoped to let the webpage be ready first and display loading image in some not ready area. And when spawned threads are ready, server will raise a event (socket) to call certain client to change from loading gif to the important images.

### need to handle different clients connection
Assume that there are many clients try to establish connection with server, server will have to manage the clients so it can  send right message and event to the right client. 

### It's better to improve thumbnails generating efficiency
I haven't come up with new idea to improve the efficiency
## Jobs to do
- - - -
### events handle (events.py)
Most of the events haven't finished yet (mainly server call client to change image, and client can change different mode of display by clicking some bottom

### route function of /\<jumboId>/\<date> (routes.py)
thumbnail/gif display webpage function haven't started

<<<<<<< HEAD
### Jobs to do

#### events handle (events.py)

#### route function of /<jumboId>/<date> (routes.py)

#### thumb_generater 
=======
### thumb_generater.py
the script is almost ready, need to be merged to the server
>>>>>>> 5b24e929ba37e4ed49672855931aec11b283cd38
