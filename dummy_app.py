import socketio
from config_fetcher.config_fetcher import fetch_config
from config_fetcher.network_config import NetworkConfig
from datatypes import commands

config = NetworkConfig(fetch_config("server"))
sio = socketio.Client()


@sio.event
def connect():
    print('connection established')


@sio.on('info', namespace='/app')
def receive_info(sid, environ):
    print(f'Received Info from server. sid: {sid} environ: {environ}')


@sio.event
def disconnect():
    print('disconnected from server')


if __name__ == "__main__":
    URL = f'http://{config.ip}:{config.ports.control}'
    print(f"Connecting to {URL}")
    sio.connect(URL, namespaces=["/app"])
    while True:
        message = input("Message: ")
        words = message.split(' ')
        print(f"Got {words}")
        payload = commands.Movement(*[int(word) for word in words])
        sio.emit('command', dict(payload), "/app")
