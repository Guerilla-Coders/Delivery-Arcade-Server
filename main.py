import subprocess

from flask import Flask, render_template
from flask_socketio import SocketIO
from config_fetcher.config_fetcher import fetch_config
from config_fetcher.network_config import NetworkConfig

config = NetworkConfig(fetch_config("server"))

app = Flask(__name__)
app.config['SECRET_KEY'] = config.secret_key
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
        config.secret_key,
        config.ports.video.post.L,
        config.ports.video.broadcast.L
    ]
]


@app.route('/video')
def sessions():
    video_broadcast_port = config.ports.video.broadcast.L
    return render_template('view-stream.html', video_broadcast_port=video_broadcast_port)


if __name__ == '__main__':
    websocket_relay_process = subprocess.Popen(websocket_relay_args, stdout=subprocess.PIPE)
    socketio.run(app, host=config.ip, port=config.ports.control, debug=True)
