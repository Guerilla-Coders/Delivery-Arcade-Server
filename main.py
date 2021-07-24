import subprocess

from flask import Flask, render_template
from flask_socketio import SocketIO
import network_definition as ndef

app = Flask(__name__)
app.config['SECRET_KEY'] = ndef.SERVER_SECRET_KEY
socketio = SocketIO(app)


@socketio.on('connect', namespace='/app')
def connect_handler(data):
    print(f'APP CONNECTED sid: {data}')


@socketio.on('connect', namespace='/agent')
def connect_handler(data):
    print(f'AGENT CONNECTED sid: {data}')


@socketio.on('connect', namespace='/')
def connect_handler(data):
    print(f'Connection request root sid: {data}')


@socketio.on('disconnect', namespace='/app')
def disconnected_handler():
    print(f'APP DISCONNECTED')


@socketio.on('disconnect', namespace='/agent')
def disconnected_handler():
    print(f'AGENT DISCONNECTED')


@socketio.on('command', namespace='/app')
def receive_command_from_app(data):
    print(f'Received command from app. sid: {data}')
    socketio.emit('command', data=data, namespace='/agent')


@socketio.on('info', namespace='/agent')
def receive_info_from_agent(data):
    print(f'Received info from agent. sid: {data}')


websocket_relay_args = [
    str(arg) for arg in [
        'node',
        'websocket-relay.js',
        ndef.SERVER_SECRET_KEY,
        ndef.SERVER_VIDEO_POST_PORT_L,
        ndef.SERVER_VIDEO_BROADCAST_PORT_L
    ]
]


@app.route('/video')
def sessions():
    video_broadcast_port = ndef.SERVER_VIDEO_BROADCAST_PORT_L
    return render_template('view-stream.html', video_broadcast_port=video_broadcast_port)


if __name__ == '__main__':
    websocket_relay_process = subprocess.Popen(websocket_relay_args, stdout=subprocess.PIPE)
    socketio.run(app, host=ndef.SERVER_IP, port=ndef.SERVER_CONTROL_PORT, debug=True)
