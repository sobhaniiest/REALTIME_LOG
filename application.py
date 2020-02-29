import time
from flask_socketio import SocketIO, emit
from flask import Flask, render_template, url_for, copy_current_request_context
from random import random
from time import sleep
from threading import Thread, Event

fp = open("/var/log/auth.log", "r")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['DEBUG'] = True

socketio = SocketIO(app, async_mode=None, logger=True, engineio_logger=True)
thread = Thread()
thread_stop_event = Event()

def get_data():
  
    while not thread_stop_event.isSet():
	global fp
        line = fp.readlines()
	socketio.emit('newnumber', {'number': line}, namespace='/test')
	socketio.sleep(10)


@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect', namespace='/test')
def test_connect():
	global thread
	print('Client connected')
	global fp

	fp.seek(0,2)
	if not thread.isAlive():
		thread = socketio.start_background_task(get_data)

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app)
