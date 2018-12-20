from flask import session , request
from flask_socketio import emit
from .. import socketio
import time


clients = {}

@socketio.on('pRequest',namespace='/ID-1C21D1C10011')
def greet(msg):
    # time.sleep(10)
    print('received :'+ msg)
    # emit('greet','hi client')

@socketio.on('clientGreet',namespace='/ID-1C21D1C10011')
def handle_connect(msg): #get jumboId
    if msg in clients:
        clients[msg].append(request.sid)
    else:   
        clients.update({msg:[request.sid]})
    print('client connected %s : %s'%(msg,request.sid))
    # emit('sdFigReady','hi')
    

@socketio.on('disconnect')
def handle_disconnect():
    print('client disconnected')
    # clients[jumboId].remove(request.sid)


def send_message(data, jumboId,broadcast=True):
    client_id=clients[jumboId][-1]
    # client_id='/'+jumboId
    emit('sdFigReady', data,room=client_id, namespace='/%s'%(jumboId))
    # socketio.sleep(0)
    print('sending message {} to {}'.format(data,client_id))