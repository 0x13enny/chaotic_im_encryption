from flask import Flask
from flask_socketio import SocketIO


socketio=SocketIO()

def initApp(debug=False):
    global app
    app = Flask(__name__)
    app.debug = debug
    from .controller import blueprint
    app.register_blueprint(blueprint)
    socketio.init_app(app)  
    return app