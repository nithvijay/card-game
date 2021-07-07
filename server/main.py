import datetime
import json
import random
import os

from utils.db_init import initial_input
from utils.db_utils import gen_main_id
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
initial_input(r)


@socketio.on("connect")
def connect():
    print(f"{request.sid} connected.\n\n\n\n")


@socketio.on("main_id")
def on_send_main_id(data):
    # check main id if it is in the database, else generate new one
    main_id = data
    if main_id in r.smembers("main_ids"):  # user exists in the database
        r.set(request.sid, main_id)
    else:
        main_id_generator = int(r.get("main_id_generator"))
        main_id = gen_main_id(main_id_generator)
        r.set("main_id_generator", main_id_generator + 1)
        r.set(request.sid, main_id)
        r.sadd("main_ids", main_id)
    emit('get_main_id', {'mainID': main_id})


@socketio.on('join')
def on_join(data):  # This is called in chatapp.js when the user submits a name in /rooms/<room>
    user = data['username']
    room = data['room']
    sid = request.sid
    main_id = r.get(sid)
    is_user_in_room_data = False

    # room exists and user was in that room
    if r.get(f"roomData:{room}"):
        room_data = get_room_data(room)
        is_user_in_room_data = main_id in room_data['userMainIDs']

    if (r.get(f"game_started:{room}") == "T") and not is_user_in_room_data:
        emit('entered_room', "Game has already started")
        # if username exists in room
    elif user in set(r.get(member) for member in list(r.smembers(f"room_members:{room}"))):
        emit('entered_room', "Username taken in that room")
    else:
        join_room_function(room, main_id, user)

def join_room_function(room, main_id, user):
    join_room(room)

    r.set(main_id, user)  # key-value pair for main_id and user name

    if r.get(f"game_started:{room}") != "T":
            emit('entered_room', "T")
    else:
        emit('entered_room', "Started Already")
        # get index of user who was in the room previously
        room_data = get_room_data(room)
        playerIndex = room_data['userMainIDs'].index(main_id)
        room_data['userNames'][playerIndex] = user
        set_room_data(room, room_data)
        emit("update_game_state", room_data, room=room)

    # so users can only be part of one room, potentially slow with large number of rooms, looping through all rooms to see
    for key in list(r.smembers("set_of_rooms")):
        if r.srem(f"room_members:{key}", main_id):
            leave_room(key)
            emit('message', {
                'message': f"{user} has left Room {key}"}, room=key)
            members = [r.get(member) for member in list(
                r.smembers(f"room_members:{key}"))]
            emit('update_room_members', {'room_occupants': members}, room=key)

    # index of keys
    # set named set_of_rooms contains all rooms
    r.sadd("set_of_rooms", room)

    # set named room_members:ASDF contains main_id of users in the room
    r.sadd(f"room_members:{room}", main_id)

    emit('message_history', {'message_history': r.lrange(
        f"room_message_history:{room}", 0, 1000)})
    emit('message', {
            'message': f"{user} has entered Room {room}"}, room=room)
    members = [r.get(member)
                for member in list(r.smembers(f"room_members:{room}"))]
    emit('update_room_members', {'room_occupants': members}, room=room)



@socketio.on("message")
def on_message(data):
    room = data['room']
    username = data['username']
    message = data['message']
    to_send = f"{datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=-5))).strftime('%I:%M:%S %p')} - {username}: {message}"
    r.lpush(f"room_message_history:{room}", to_send)

    emit('message', {'message': to_send}, room=room)


@socketio.on('disconnect')
def on_disconnect():
    sid = request.sid
    main_id = r.get(sid)
    print("/n/n/n/n/n asf asdf asf")
    print(main_id)
    
    for key in list(r.smembers("set_of_rooms")):
        # check which room the user left
        if r.srem(f"room_members:{key}", main_id):
            emit('message', {
                 'message': f"{r.get(main_id)} has left Room {key}"}, room=key)
            members = [r.get(member) for member in list(
                r.smembers(f"room_members:{key}"))]
            emit('update_room_members', {'room_occupants': members}, room=key)
    r.delete(sid)


@socketio.on('delete_history')
def delete_history(data):
    for key in r.keys():
        r.delete(key)
    initial_input(r)


################
## Game Logic ##
################
CARD_START_ID = 0
NUM_CARDS = 3
WIN_SCORE = 10
MAX_ENERGY = 10
AUTOGEN_ENERGY = 3


def get_room_data(room):
    return json.loads(r.get(f"roomData:{room}"))


def set_room_data(room, room_data):
    r.set(f"roomData:{room}", json.dumps(room_data))


@socketio.on('start_game')
def start_game(room):
    emit("game_started", "", room=room)
    r.set(f"game_started:{room}", "T")
    room_data = dict()
    userMainIDs = [member for member in list(
        r.smembers(f"room_members:{room}"))]
    userNames = [r.get(mainID) for mainID in userMainIDs]
    userEnergies = [MAX_ENERGY for _ in userMainIDs]
    scores = [0 for _ in userMainIDs]
    playedThisTurn = [False for _ in userMainIDs]
    turn = 0
    centerCards = []
    centerCardsPlayerIndex = []
    userCards = []
    lastRoundDesc = "Select a card to begin"
    totalNumberOfRounds = 1

    r.set(f"room_card_id:{room}", CARD_START_ID)

    cards = [r.hgetall(f"card:{key}")
             for key in list(r.smembers("card_index"))]

    for _ in userMainIDs:
        rand_cards = random.choices(cards, k=NUM_CARDS)
        player_cards = []
        for card in rand_cards:
            card_id = r.get(f"room_card_id:{room}")
            r.set(f"room_card_id:{room}", int(card_id) + 1)
            card['id'] = card_id
            player_cards.append(card.copy())
        userCards.append(player_cards)

    room_data = {
        "userCards": userCards,
        "centerCards": centerCards,
        "userNames": userNames,  # ordered
        "userEnergies": userEnergies,
        "userMainIDs": userMainIDs,
        "scores": scores,
        "turn": turn,
        "maxEnergy": MAX_ENERGY,
        "playedThisTurn": playedThisTurn,
        "centerCardsPlayerIndex": centerCardsPlayerIndex,
        "lastRoundDesc": lastRoundDesc,
        "totalNumberOfRounds": totalNumberOfRounds
    }
    set_room_data(room, room_data)
    emit("update_game_state", room_data, room=room)


# this function needs a lot of rework into smaller utility functions
@socketio.on('played card')
def played_card(data):
    id = data['id']
    room = data['room']

    room_data = get_room_data(room)
    userCards = room_data['userCards']

    user_index = get_user_played_card(userCards, id)

    if not room_data['playedThisTurn'][user_index]:  # if the user hasn't gone that round
        players_cards = userCards[user_index]
        played_card_index = [i for i, card in enumerate(
            players_cards) if card['id'] == id][0]

        # user plays card that they have the energy for
        if room_data['userEnergies'][user_index] >= int(players_cards[played_card_index]['cost']):
            # TODO: Come up with a better system

            room_data['centerCards'].append(players_cards[played_card_index])
            room_data['centerCardsPlayerIndex'].append(user_index)
            room_data['userEnergies'][user_index] = min(AUTOGEN_ENERGY + int(
                room_data['userEnergies'][user_index]) - int(players_cards[played_card_index]['cost']), MAX_ENERGY)
            room_data['userCards'][user_index].pop(played_card_index)
            room_data['userCards'][user_index].append(
                gen_random_card(room, room_data['userEnergies'][user_index]))
            room_data['playedThisTurn'][user_index] = True

            # if all users have played
            if all(room_data['playedThisTurn']):
                # handle game condition
                winner_index = get_winner(
                    centerCards=room_data['centerCards'],
                    centerCardsPlayerIndex=room_data['centerCardsPlayerIndex']
                )
                if winner_index != -1:
                    winner_name = room_data['userNames'][winner_index]
                    room_data['scores'][winner_index] += 1
                    room_data['lastRoundDesc'] = f"{winner_name} won last round!"
                else:
                    room_data['lastRoundDesc'] = "It was a tie"

                room_data['totalNumberOfRounds'] += 1
                room_data['centerCards'] = []
                room_data['centerCardsPlayerIndex'] = []
                room_data['playedThisTurn'] = [
                    False for _ in room_data['playedThisTurn']]

                if room_data['scores'][winner_index] == WIN_SCORE:
                    emit("win_game", room_data['userNames']
                         [winner_index], room=room)
                    r.set(f"game_started:{room}", "F")

            set_room_data(room, room_data)
            emit("update_game_state", room_data, room=room)


def get_user_played_card(userCards, id):
    for i, cards in enumerate(userCards):
        if id in [card['id'] for card in cards]:
            return i  # index of user who played the card


def get_winner(centerCards, centerCardsPlayerIndex):
    attacks = [int(card['attack']) for card in centerCards]
    highest_attack = max(attacks)
    # indicates tie
    tie = sum(attack == highest_attack for attack in attacks) > 1
    # index of winner card
    return -1 if tie else centerCardsPlayerIndex[attacks.index(highest_attack)]


def gen_random_card(room, userEnergy):
    cards = [r.hgetall(f"card:{key}")
             for key in list(r.smembers("card_index"))]
    filtered_cards = [card for card in cards if (
        int(card['cost']) <= userEnergy)]
    card_id = r.get(f"room_card_id:{room}")
    r.set(f"room_card_id:{room}", int(card_id) + 1)
    card = random.choice(filtered_cards)
    card['id'] = card_id
    return card


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')  # eventlet will be used, it
