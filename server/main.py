import random
import os

import eventlet
from flask.helpers import get_env
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
        remove_player_from_room(pid, last_active_room)
        room_lobby_status = db.get_json(
            f'room_lobby_status:{last_active_room}')
        db.delete(f"last_active_room:{pid}")
        # no game started and no one in room
        if not room_lobby_status['started'] and len(room_lobby_status['members']) == 0:
            db.delete(f'room_lobby_status:{last_active_room}')
            db.srem("set_of_rooms", last_active_room)
            db.delete(f'general_game_data:{last_active_room}')


def remove_player_from_room(pid, room):
    leave_room(room)
    room_lobby_status = db.get_json(f'room_lobby_status:{room}')
    new_room_lobby_status_members = [
        member for member in room_lobby_status['members'] if member['pid'] != pid]
    room_lobby_status['members'] = new_room_lobby_status_members
    db.set_json(f'room_lobby_status:{room}', room_lobby_status)
    emit("updateRoomLobbyStatus", room_lobby_status, room=room)


@socketio.on("pageLoaded")
def on_page_loaded(pid):
    if db.sismember('set_of_pids', pid):  # if pid exists in database
        emit('setPid', pid)
        db.set(request.sid, pid)
    else:  # need to generate new pid
        pid = gen_random_pid(db)
        emit('setPid', pid)
        db.set(request.sid, pid)

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
        if room_lobby_status['started']:
            general_game_data = db.get_json(f'general_game_data:{room}')

            doesPidExist, user_index = check_if_pid_exists_in_room(
                general_game_data, pid)
            if doesPidExist:  # if pid in the room, accept and change username
                if general_game_data['usernames'][user_index] == username:  # same username
                    user_rejoin_room(db, pid, username, room,
                                     user_index=user_index)
                # different username and taken
                elif check_if_username_taken(room_lobby_status, username):
                    emit('errorLoggingIn', {
                        'type': 'username',
                        'errorMessage': 'Username already taken in that room'
                    })
                else:  # different username
                    user_rejoin_room(db, pid, username, room,
                                     user_index=user_index)
            else:  # else return error message
                emit('errorLoggingIn', {
                    'type': 'room',
                    'errorMessage': 'Game already started in that room'
                })
        elif check_if_username_taken(room_lobby_status, username):
            emit('errorLoggingIn', {
                'type': 'username',
                'errorMessage': 'Username already taken in that room'
            })
        else:  # room exists and user can enter room
            add_user_to_room(db, pid, username, room)


def add_user_to_room(db, pid, username, room, set_view=True):
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
    if set_view:
        emit("setPageView", 'room-lobby-view')


def user_rejoin_room(db, pid, username, room, user_index):
    add_user_to_room(db, pid, username, room, set_view=False)

    general_game_data = db.get_json(f'general_game_data:{room}')
    general_game_data['usernames'][user_index] = username  # update username
    db.set_json(f"general_game_data:{room}", general_game_data)

    emit('updateGeneralGameData', general_game_data, room=room)
    emit('updateUserIndex')  # only for user?
    emit('initializeCardsSelected',
         general_game_data['gameConfig']['numCardsInHand'])

    for stage_num in range(1, int(general_game_data['stage']) + 1):
        stage_data = db.get_json(f'stage_{stage_num}_data:{room}')
        # TODO: only emit to user?
        emit(f'updateStage{stage_num}Data', stage_data)
    emit("setPageView", 'game-view')


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

    if (len(room_lobby_status['members']) >= 3) and all_ready:
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
    emit('initializeCardsSelected',
         max_num_cards_in_hand, room=room)

    db.set_json(f'stage_1_data:{room}', stage_1_data)
    emit('updateStage1Data', stage_1_data, room=room)
    emit("setPageView", "game-view", room=room)


def gen_cards(CARDS, max_num, num_in_hand, db, room):
    ret_cards = []
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

    room_lobby_status['config'][setting] = value
    db.set_json(f"room_lobby_status:{room}", room_lobby_status)
    # slightly more efficient than sending entire room_lobby_status? however, when room_lobby_status updates from players getting ready, the roomConfig will also update
    emit("updateRoomConfig", {'setting': setting, 'value': value}, room=room)


@socketio.on("returnToLogin")
def on_return_to_login(data):
    room = data['room']
    pid = data['pid']
    remove_player_from_room(pid, room)
    emit("setPageView", 'login-view')

#####
# Stage 1
#####


@socketio.on("stage1UserReady")
def on_stage_1_user_ready(data):
    pid = data['pid']
    room = data['room']
    cards_selected_ids = data['cardsSelectedIds']

    general_game_data = db.get_json(f'general_game_data:{room}')
    user_index = general_game_data['pids'].index(pid)

    stage_1_data = db.get_json(f'stage_1_data:{room}')
    stage_1_data['isReady'][user_index] = True
    db.set_json(f'stage_1_data:{room}', stage_1_data)
    emit('updateStage1Data', stage_1_data, room=room)
    fulfill_discard(db, cards_selected_ids, user_index, room)

    if all(stage_1_data['isReady']):
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
    emit('initializeCardsSelected',
         general_game_data['gameConfig']['numCardsInHand'])

#####
# Stage 2
#####


def start_stage_2(db, room):
    general_game_data = db.get_json(f'general_game_data:{room}')
    general_game_data['stage'] = 2
    db.set_json(f'general_game_data:{room}', general_game_data)

    is_ready = [False for _ in general_game_data['pids']]
    num_cards_for_each_user = [0 for _ in general_game_data['pids']]
    cards_chosen = [[] for _ in general_game_data['pids']]

    inspector_index = int(general_game_data['inspectorIndex'])
    is_ready[inspector_index] = True
    stage_2_data = {
        'isReady': is_ready,
        'numCardsForEachUser': num_cards_for_each_user,
        'cardsChosen': cards_chosen
    }
    db.set_json(f'stage_2_data:{room}', stage_2_data)
    emit('updateStage2Data', stage_2_data, room=room)
    emit('updateGeneralGameData', general_game_data, room=room)
    emit('initializeCardsSelected',
         general_game_data['gameConfig']['numCardsInHand'])


@socketio.on("stage2SelectCard")
def on_stage_2_user_ready(data):
    user_index = data['userIndex']
    room = data['room']
    num_cards = data['numCards']

    stage_2_data = db.get_json(f'stage_2_data:{room}')
    stage_2_data['numCardsForEachUser'][user_index] = num_cards
    db.set_json(f'stage_2_data:{room}', stage_2_data)
    emit('updateStage2Data', stage_2_data, room=room)


@socketio.on("stage2UserReady")
def on_stage_2_user_ready(data):
    pid = data['pid']
    room = data['room']
    cards_selected_ids = data['cardsSelectedIds']

    # emit('debug', {
    #     "pid": pid,
    #     "room": room,
    #     "cards_selected_ids": cards_selected_ids
    # })

    general_game_data = db.get_json(f'general_game_data:{room}')
    user_index = general_game_data['pids'].index(pid)

    stage_2_data = db.get_json(f'stage_2_data:{room}')

    stage_2_data['cardsChosen'][user_index] = cards_selected_ids
    stage_2_data['isReady'][user_index] = True

    db.set_json(f'stage_2_data:{room}', stage_2_data)
    emit('updateStage2Data', stage_2_data, room=room)

    if all(stage_2_data['isReady']):
        start_stage_3(db, room)

#####
# Stage 3
#####


def start_stage_3(db, room):
    general_game_data = db.get_json(f'general_game_data:{room}')
    general_game_data['stage'] = 3

    stage_2_data = db.get_json(f'stage_2_data:{room}')
    cards_chosen = stage_2_data['cardsChosen']

    cards_in_bag = move_cards(cards_chosen, general_game_data)
    db.set_json(f'general_game_data:{room}', general_game_data)

    inspector_decisions = ['' for _ in general_game_data['pids']]
    is_checked = [False for _ in general_game_data['pids']]
    inspector_index = int(general_game_data['inspectorIndex'])
    is_checked[inspector_index] = True

    stage_3_data = {
        'isChecked': is_checked,
        'inspectorDecisions': inspector_decisions,
        'cardsInBag': cards_in_bag
    }
    db.set_json(f'stage_3_data:{room}', stage_3_data)
    emit('updateStage3Data', stage_3_data, room=room)
    emit('updateGeneralGameData', general_game_data, room=room)
    # emit('debug', {
    #     "stage_3_data": stage_3_data,
    #     "general_game_data": general_game_data,
    # })


def move_cards(cards_chosen, general_game_data):
    cards_in_bag = []
    for user_index, users_cards in enumerate(general_game_data['cards']):
        cards_in_bag_user = []
        indexer = 0
        for _ in range(len(users_cards)):
            if users_cards[indexer]['id'] in set(cards_chosen[user_index]):
                cards_in_bag_user.append(users_cards[indexer])
                users_cards.pop(indexer)
            else:
                indexer += 1
        cards_in_bag.append(cards_in_bag_user)
    return cards_in_bag


@socketio.on("stage3MakeDecision")
def on_stage_3_make_decision(data):
    pid = data['pid']
    room = data['room']
    option = data['option']

    # emit("debug", {
    #     "pid": pid,
    #     "room": room,
    #     "option": option
    # })

    stage_3_data = db.get_json(f'stage_3_data:{room}')
    general_game_data = db.get_json(f'general_game_data:{room}')

    user_index = general_game_data['pids'].index(pid)
    stage_3_data['isChecked'][user_index] = True
    stage_3_data['inspectorDecisions'][user_index] = option

    db.set_json(f'stage_3_data:{room}', stage_3_data)

    emit('updateStage3Data', stage_3_data, room=room)


@socketio.on("stage3Ready")
def on_stage_3_user_ready(data):
    # only the inspector declares stage is ready
    room = data['room']

    # emit('debug', {"status": 'stage_3_ready'})

    general_game_data = db.get_json(f'general_game_data:{room}')
    general_game_data['stage'] = 4

    stage_3_data = db.get_json(f'stage_3_data:{room}')

    scoring_data = [{} for _ in general_game_data['pids']]
    inspector_data = []

    inspector_index = general_game_data['inspectorIndex']

    for index, decision in enumerate(stage_3_data['inspectorDecisions']):
        if index != inspector_index:
            cards_in_bag_for_user = stage_3_data['cardsInBag'][index]

            card_data = calculate_cards(cards_in_bag_for_user)
            score = card_data['score']
            is_positive = None

            if decision == 'let go':
                is_positive = True
                general_game_data['scores'][index] += score
            else:  # decision == 'inspected'
                # any contraband
                if (any(card['type'] == 'Contraband' for card in cards_in_bag_for_user)):
                    is_positive = False
                    general_game_data['scores'][index] -= score
                    general_game_data['scores'][inspector_index] += score
                else:  # no contraband
                    is_positive = True
                    general_game_data['scores'][index] += score
                    general_game_data['scores'][inspector_index] -= score

                inspector_data.append({
                    'isPositive': not is_positive,
                    'score': score,
                    'cardCounts': card_data['card_counts'],
                    'keys': card_data['keys'],
                    'index': index
                })

            scoring_data[index] = {
                'isPositive': is_positive,
                'score': score,
                'cardCounts': card_data['card_counts'],
                'keys': card_data['keys']
            }

    if check_win(general_game_data):
        emit('debug', {"status": 'check_win'})
        general_game_data['stage'] = 5
        winner_index = get_winner(general_game_data)
        stage_5_data = {
            'winnerIndex': winner_index,
            'sortedScoresIndex': return_rankings(general_game_data['scores'])
        }
        db.set_json(f'general_game_data:{room}', general_game_data)
        db.set_json(f'stage_5_data:{room}', stage_5_data)

        emit('updateStage5Data', stage_5_data, room=room)
        emit('updateGeneralGameData', general_game_data, room=room)

        room_lobby_status = db.get_json(f"room_lobby_status:{room}")
        room_lobby_status['started'] = False
        for member in room_lobby_status['members']:
            member['isReady'] = False
        db.set_json(f"room_lobby_status:{room}", room_lobby_status)
        emit("updateRoomLobbyStatus", room_lobby_status, room=room)

    else:
        stage_4_data = {
            'scoringData': format_cards(inspector_index, scoring_data, inspector_data, general_game_data),
            'isReady': [False for _ in general_game_data['pids']]
        }

        db.set_json(f'general_game_data:{room}', general_game_data)
        db.set_json(f'stage_4_data:{room}', stage_4_data)

        emit('updateStage4Data', stage_4_data, room=room)
        emit('updateGeneralGameData', general_game_data, room=room)
        emit('debug', {
            "stage_4_data": stage_4_data,
            "general_game_data": general_game_data,
        })


def calculate_cards(cards_in_bag_for_user):
    to_ret = {
        'score': 0,
        'card_counts': {}
    }
    for card in cards_in_bag_for_user:
        if to_ret['card_counts'].get(card['name']):
            to_ret['card_counts'][card['name']]['quantity'] += 1
        else:
            to_ret['card_counts'][card['name']] = {
                'value': card['value'],
                'quantity': 1
            }
        to_ret['score'] += card['value']
    to_ret['keys'] = sorted(to_ret['card_counts'].keys())
    return to_ret


def format_cards(inspector_index, scoring_data, inspector_data, general_game_data):
    to_ret = []
    for index, user in enumerate(scoring_data):
        user_data = []
        if index == inspector_index:
            for set_of_cards in inspector_data:
                inspector_resources = []
                for key in set_of_cards['keys']:
                    new_resource = set_of_cards['cardCounts'][key].copy()
                    new_resource['name'] = key
                    new_resource['sign'] = "+" if set_of_cards['isPositive'] else "-"
                    new_resource['username'] = general_game_data['usernames'][set_of_cards['index']]
                    inspector_resources.append(new_resource)
                user_data.append(inspector_resources)
        else:
            for key in user['keys']:
                new_resource = user['cardCounts'][key]
                new_resource['name'] = key
                new_resource['sign'] = "+" if user['isPositive'] else "-"
                user_data.append(new_resource)
        to_ret.append(user_data)
    return to_ret


def check_win(general_game_data):
    score_to_win = int(general_game_data['gameConfig']['scoreToWin'])
    return any(int(score) >= score_to_win for score in general_game_data['scores'])


def get_winner(general_game_data):
    emit('debug', {"status": general_game_data['scores']})
    int_scores = [int(score) + 1 for score in general_game_data['scores']]
    max_score = max(int_scores)
    winning_user_indices = [user_index for user_index,
                            score in enumerate(int_scores) if score == max_score]

    if len(winning_user_indices) > 1:  # multiple winners
        total_card_values = []
        for user_index in winning_user_indices:
            card_values = sum(int(card['value'])
                              for card in general_game_data['cards'][user_index])
            total_card_values.append(card_values)
        winner_index = total_card_values.index(max(total_card_values))
        return winning_user_indices[winner_index]
    else:
        emit("debug", {'status': 'one_winner'})
        return winning_user_indices[0]


def return_rankings(scores):
    return sorted(range(len(scores)), key=lambda k: -int(scores[k]))

######
# Stage 4
######


@socketio.on("stage4UserReady")
def on_stage_4_user_ready(data):
    pid = data['pid']
    room = data['room']

    general_game_data = db.get_json(f'general_game_data:{room}')
    user_index = general_game_data['pids'].index(pid)

    stage_4_data = db.get_json(f'stage_4_data:{room}')
    stage_4_data['isReady'][user_index] = True
    db.set_json(f'stage_4_data:{room}', stage_4_data)
    emit('updateStage4Data', stage_4_data, room=room)

    if all(stage_4_data['isReady']):
        general_game_data['inspectorIndex'] = (
            int(general_game_data['inspectorIndex']) + 1) % len(general_game_data['pids'])
        general_game_data['stage'] = 1
        db.set_json(f'general_game_data:{room}', general_game_data)
        start_stage_1(db, room)


#####
# Stage 5
#####

@socketio.on("stage5GoToLobby")
def on_stage_5_go_to_lobby(data):
    emit("setPageView", 'room-lobby-view')


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')  # eventlet will be used, it
