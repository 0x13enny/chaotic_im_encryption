# import eventlet
# eventlet.monkey_patch()
from app import initApp, socketio
import random, webbrowser, subprocess
# import eventlet


if __name__ == '__main__':
    app = initApp(debug=True)
    host='0.0.0.0'
    # port = 5000 + random.randint(0, 999)
    port = 5000 #debug mode
    # url = "http://{}:{}".format(host,port)  #ID-a test
    # browser = subprocess.Popen(['firefox', url])
    # webbrowser.open(url)
    
    socketio.run(app,host=host,port=port)
    subprocess.Popen('rm -f app/tmp/* ;rm -rf app/static/image_generated/*',shell=True)
    # browser.terminate()