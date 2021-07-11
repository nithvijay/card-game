import os

import eventlet
import redis
from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room

from utils.db_init import init_database
from utils.db_utils import clear_database, gen_random_pid
from database_wrapper import DB

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
db = DB(r)
clear_database(db)
init_database(db)


@socketio.on("connect")
def on_connect():
    print(f"{request.sid} connected.\n\n\n\n")


@socketio.on("disconnect")
def on_disconnect():
    pid = db.get(request.sid)
    db.delete(request.sid)
    db.delete(request.sid)

    if db.exists(f"last_active_room:{pid}"):
        last_active_room = db.get(f"last_active_room:{pid}")
        room_lobby_status = db.get_json(
            f'room_lobby_status:{last_active_room}')
        new_room_lobby_status_members = [
            member for member in room_lobby_status['members'] if member['pid'] != pid]
        room_lobby_status['members'] = new_room_lobby_status_members
        db.set_json(f'room_lobby_status:{last_active_room}', room_lobby_status)
        db.delete(f"last_active_room:{pid}")
        # no game started and no one in room
        if not room_lobby_status['started'] and len(new_room_lobby_status_members) == 0:
            db.delete(f'room_lobby_status:{last_active_room}')
            db.srem("set_of_rooms", last_active_room)
            # TODO: db.delete(f'room_game_data:{last_active_room}')


@socketio.on("pageLoaded")
def on_page_loaded(pid):
    if db.sismember('set_of_pids', pid):  # if pid exists in database
        emit('setPid', pid)
        db.set(request.sid, pid)
        # TODO: other logic if returning user, e.g. setting other state
    else:  # need to generate new pid
        new_pid = gen_random_pid(db)
        emit('setPid', new_pid)
        db.set(request.sid, new_pid)

    emit('debug', {"sid": request.sid, "pid": pid})

####
# Login
####


@socketio.on("submitLoginInfo")
def on_submit_login_info(data):
    username = data['username']
    room = data['room']
    pid = data['pid']

    # 1. check if pid was in the room
    # 1. update username in room and emit game state
    # 2. update user's game state and return to put them where they were
    # 2. else check if room has started game
    # True - game has already started - error message
    # 3. else check if user in room has same user name
    # True - username is taken - error message
    # 4. else user can enter room
    if not db.exists(f"room_lobby_status:{room}"):  # room does not exist
        db.sadd("set_of_rooms", room)

        room_lobby_status = {}
        room_lobby_status['started'] = False
        room_lobby_status['members'] = []
        db.set_json(f"room_lobby_status:{room}", room_lobby_status)

        add_user_to_room(db, pid, username, room)
    elif False:  # TODO room has started game and pid was in the room
        pass
    elif False:  # TODO room has started game
        pass
    elif False:  # TODO someone in room has same user name
        pass
    else:  # room exists and user can enter room
        add_user_to_room(db, pid, username, room)


def add_user_to_room(db, pid, username, room):
    room_lobby_status = db.get_json(f"room_lobby_status:{room}")
    db.set(pid, username)
    # db.sadd(f"active_room_members:{room}", pid)
    room_lobby_status['members'].append({
        'pid': pid,
        'username': username,
        'isReady': False
    })
    join_room(room)
    emit("setPageView", "room-lobby")
    db.set_json(f"room_lobby_status:{room}", room_lobby_status)
    emit("updateRoomLobbyStatus", room_lobby_status, room=room)
    db.set(f"last_active_room:{pid}", room)

######
# Room Lobby
######


@socketio.on("changeReadyStatusRoomLobby")
def on_change_ready_status_room_lobby(data):
    pid = data['pid']
    room = data['room']
    isReady = data['isReady']
    room_lobby_status = db.get_json(f"room_lobby_status:{room}")

    emit('debug', {"room_lobby_status": room_lobby_status.sid,
         "isReady": isReady})

    # emit("updateRoomLobbyStatus", room_lobby_status, room=room)
    pass


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')  # eventlet will be used, it
