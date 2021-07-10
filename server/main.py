import os

import eventlet
import redis
from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room

eventlet.monkey_patch()

app = Flask(__name__)

# ENV Variables
ENVIRONMENT = os.getenv('ENVIRONMENT', 'DEV')
AWS_ADDRESS = os.environ.get('AWS_ADDRESS')
REDIS_ADDRESS = os.getenv('REDIS_ADDRESS', 'redis')

cors_allowed_origins = ['http://localhost:3000',
                        'http://localhost:8080'] if ENVIRONMENT == 'DEV' else [AWS_ADDRESS]

socketio = SocketIO(app, cors_allowed_origins=cors_allowed_origins,
                    async_handlers=True, async_mode='eventlet')  # , message_queue="redis://redis:6379")
r = redis.Redis(host=REDIS_ADDRESS, port=6379, db=0, decode_responses=True)


@socketio.on("connect")
def connect():
    print(f"{request.sid} connected.\n\n\n\n")
    emit('customEmit', request.sid)


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')  # eventlet will be used, it
