import random
import os

import eventlet
import redis
from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room

from utils.db_init import init_database
from utils.db_utils import clear_database, gen_random_pid, CARDS
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

    if db.exists(f"last_active_room:{pid}"):
        last_active_room = db.get(f"last_active_room:{pid}")
        room_lobby_status = db.get_json(
            f'room_lobby_status:{last_active_room}')
        new_room_lobby_status_members = [
            member for member in room_lobby_status['members'] if member['pid'] != pid]
        room_lobby_status['members'] = new_room_lobby_status_members
        db.set_json(f'room_lobby_status:{last_active_room}', room_lobby_status)
        emit("updateRoomLobbyStatus", room_lobby_status, room=last_active_room)

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


@socketio.on("delete")
def on_delete():
    clear_database(db)
    init_database(db)

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
        # come up with better system for initial values
        room_lobby_status['config'] = {
            'scoreToWin': '50', 'numCardsInHand': '3'}
        db.set_json(f"room_lobby_status:{room}", room_lobby_status)

        add_user_to_room(db, pid, username, room)
    else:  # room exists
        room_lobby_status = db.get_json(f"room_lobby_status:{room}")
        emit('debug', {"status": 'room exists'})
        if room_lobby_status['started']:  # TODO room has started game
            general_game_data = db.get_json(f'general_game_data:{room}')

            doesPidExist, user_index = check_if_pid_exists_in_room(
                general_game_data, pid)
            if doesPidExist:  # if pid in the room, accept and change username
                if check_if_username_taken(room_lobby_status, username):
                    emit('debug', {"status": 'game started, username taken'})
                    emit('errorLoggingIn', {
                        'type': 'username',
                        'errorMessage': 'Username already taken in that room'
                    })
                else:
                    emit('debug', {"status": 'rejoined room'})
                    user_rejoin_room(db, pid, username, room,
                                     user_index=user_index)
            else:  # else return error message
                emit('debug', {"status": 'game started'})
                emit('errorLoggingIn', {
                    'type': 'room',
                    'errorMessage': 'Game already started in that room'
                })
        elif check_if_username_taken(room_lobby_status, username):
            emit('debug', {"status": 'username taken'})
            emit('errorLoggingIn', {
                'type': 'username',
                'errorMessage': 'Username already taken in that room'
            })
        else:  # room exists and user can enter room
            emit('debug', {"status": 'can enter'})
            add_user_to_room(db, pid, username, room)


def add_user_to_room(db, pid, username, room, view='room-lobby-view'):
    room_lobby_status = db.get_json(f"room_lobby_status:{room}")
    db.set(pid, username)
    # db.sadd(f"active_room_members:{room}", pid)
    room_lobby_status['members'].append({
        'pid': pid,
        'username': username,
        'isReady': False
    })
    db.set_json(f"room_lobby_status:{room}", room_lobby_status)

    join_room(room)
    db.set(f"last_active_room:{pid}", room)

    emit("updateRoomLobbyStatus", room_lobby_status, room=room)
    emit("setPageView", view)


def user_rejoin_room(db, pid, username, room, user_index):
    add_user_to_room(db, pid, username, room, view='game-view')

    general_game_data = db.get_json(f'general_game_data:{room}')
    general_game_data['usernames'][user_index] = username  # update username
    db.set_json(f"general_game_data:{room}", general_game_data)

    emit('updateGeneralGameData', general_game_data, room=room)
    emit('updateUserIndex')  # only for user?

    emit('debug', {"status": 'before for-loop rejoining room'})
    for stage_num in range(1, int(general_game_data['stage']) + 1):
        stage_data = db.get_json(f'stage_{stage_num}_data:{room}')
        # TODO: only emit to user?
        emit(f'updateStage{stage_num}Data', stage_data)


def check_if_username_taken(room_lobby_status, username):
    for member in room_lobby_status['members']:
        if member['username'] == username:
            return True
    return False


def check_if_pid_exists_in_room(general_game_data, pid):
    # TODO: change this to use list.index
    for index, list_pid in enumerate(general_game_data['pids']):
        if list_pid == pid:
            return True, index
    return False, None

######
# Room Lobby
######


@socketio.on("changeReadyStatusRoomLobby")
def on_change_ready_status_room_lobby(data):
    pid = data['pid']
    room = data['room']
    isReady = data['isReady']
    room_lobby_status = db.get_json(f"room_lobby_status:{room}")

    all_ready = True
    for member in room_lobby_status['members']:
        if member['pid'] == pid:
            member['isReady'] = isReady
        all_ready = all_ready and member['isReady']

    if all_ready:
        start_new_game(db, room, room_lobby_status)
        start_stage_1(db, room)

    else:
        db.set_json(f"room_lobby_status:{room}", room_lobby_status)
        emit("updateRoomLobbyStatus", room_lobby_status, room=room)


def start_new_game(db, room, room_lobby_status):
    room_lobby_status['started'] = True
    db.set_json(f"room_lobby_status:{room}", room_lobby_status)

    game_config = room_lobby_status['config']
    stage = 1
    pids = [member['pid'] for member in room_lobby_status['members']]
    usernames = [member['username'] for member in room_lobby_status['members']]
    cards = [[] for _ in pids]
    scores = [0 for _ in pids]
    inspector = 0  # eventually make random

    general_game_data = {
        'gameConfig': game_config,
        'stage': stage,
        'pids': pids,
        'usernames': usernames,
        'cards': cards,
        'scores': scores,
        'inspectorIndex': inspector
    }
    db.set(f'card_id_start:{room}', "1")
    db.set_json(f'general_game_data:{room}', general_game_data)
    emit("setPageView", "game-view", room=room)


def start_stage_1(db, room):
    general_game_data = db.get_json(f'general_game_data:{room}')
    max_num_cards_in_hand = general_game_data['gameConfig']['numCardsInHand']
    general_game_data['cards'] = [(user_cards_in_hand + gen_cards(CARDS, max_num_cards_in_hand, len(
        user_cards_in_hand), db, room)) for user_cards_in_hand in general_game_data['cards']]

    is_ready = [False for _ in general_game_data['pids']]
    inspectorIndex = int(general_game_data['inspectorIndex'])
    is_ready[inspectorIndex] = True
    stage_1_data = {
        'isReady': is_ready
    }

    db.set_json(f'general_game_data:{room}', general_game_data)
    emit('updateGeneralGameData', general_game_data, room=room)
    emit('updateUserIndex', room=room)

    db.set_json(f'stage_1_data:{room}', stage_1_data)
    emit('updateStage1Data', stage_1_data, room=room)


def gen_cards(CARDS, max_num, num_in_hand, db, room):
    ret_cards = []
    emit('debug', {
        'max_num': max_num,
        'num_in_hand': num_in_hand
    })
    for _ in range(int(max_num) - int(num_in_hand)):
        card = random.choice(CARDS).copy()
        card_id_start = db.get(f'card_id_start:{room}')
        card['id'] = card_id_start
        db.set(f'card_id_start:{room}', int(card_id_start) + 1)
        ret_cards.append(card)
    return ret_cards


@socketio.on("changeRoomConfig")
def on_change_score_to_win(data):
    room = data['room']
    setting = data['setting']
    value = data['value']
    room_lobby_status = db.get_json(f"room_lobby_status:{room}")
    emit('debug', {
        "room": room,
        "setting": setting,
        "value": value
    })

    room_lobby_status['config'][setting] = value
    db.set_json(f"room_lobby_status:{room}", room_lobby_status)
    # slightly more efficient than sending entire room_lobby_status? however, when room_lobby_status updates from players getting ready, the roomConfig will also update
    emit("updateRoomConfig", {'setting': setting, 'value': value}, room=room)

#####
# Stage 1
#####


@socketio.on("stage1UserReady")
def on_stage_1_user_ready(data):
    pid = data['pid']
    room = data['room']
    cards_selected_ids = data['cardsSelectedIds']

    emit('debug', {
        "pid": pid,
        "room": room,
        "cards_selected_ids": cards_selected_ids
    })
    # TODO: get this from client for one less db call?
    general_game_data = db.get_json(f'general_game_data:{room}')
    user_index = general_game_data['pids'].index(pid)

    stage_1_data = db.get_json(f'stage_1_data:{room}')
    stage_1_data['isReady'][user_index] = True
    db.set_json(f'stage_1_data:{room}', stage_1_data)
    emit('updateStage1Data', stage_1_data, room=room)
    fulfill_discard(db, cards_selected_ids, user_index, room)

    if all(stage_1_data['isReady']):
        # go to next stage
        emit('debug', {
            "status": "start_stage_2"
        })
        start_stage_2(db, room)


def fulfill_discard(db, cards_selected_ids, user_index, room):
    general_game_data = db.get_json(f'general_game_data:{room}')
    user_cards = general_game_data['cards'][user_index]
    max_num_cards_in_hand = general_game_data['gameConfig']['numCardsInHand']
    not_discarded = [card for card in user_cards if card['id']
                     not in set(cards_selected_ids)]
    general_game_data['cards'][user_index] = not_discarded + gen_cards(CARDS, max_num_cards_in_hand, len(
        not_discarded), db, room)
    db.set_json(f'general_game_data:{room}', general_game_data)
    emit('updateGeneralGameData', general_game_data, room=room)
    emit('updateUserIndex')  # only for user?

#####
# Stage 2
#####


def start_stage_2(db, room):
    general_game_data = db.get_json(f'general_game_data:{room}')
    general_game_data['stage'] = 2
    db.set_json(f'general_game_data:{room}', general_game_data)

    is_ready = [False for _ in general_game_data['pids']]
    num_cards_for_each_user = [0 for _ in general_game_data['pids']]

    inspectorIndex = int(general_game_data['inspectorIndex'])
    is_ready[inspectorIndex] = True
    stage_2_data = {
        'isReady': is_ready,
        'numCardsForEachUser': num_cards_for_each_user
    }
    db.set_json(f'stage_2_data:{room}', stage_2_data)
    emit('updateStage2Data', stage_2_data, room=room)
    emit('updateGeneralGameData', general_game_data, room=room)


@socketio.on("stage2UserReady")
def on_stage_2_user_ready(data):
    pid = data['pid']
    room = data['room']
    cards_selected_ids = data['cardsSelectedIds']

    emit('debug', {
        "pid": pid,
        "room": room,
        "cards_selected_ids": cards_selected_ids
    })


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')  # eventlet will be used, it
