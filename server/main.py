import datetime
import json
import random
import os

from utils.db_init import initial_input
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


@socketio.on('join')
def on_join(data):  # This is called in chatapp.js when the user submits a name in /rooms/<room>
    user = data['username']
    room = data['room']
    sid = request.sid

    if r.get(f"game_started:{room}") == "T":
        emit('entered_room', "Game has already started")
    elif user in set(r.get(member) for member in list(r.smembers(f"room_members:{room}"))):
        emit('entered_room', "Username taken in that room")
    else:
        join_room(room)
        emit('entered_room', "T")

        # index of keys
        # set named set_of_rooms contains all rooms
        r.sadd("set_of_rooms", room)
        # so users can only be part of one room, potentially slow with large number of rooms, looping through all rooms to see
        for key in list(r.smembers("set_of_rooms")):
            if r.srem(f"room_members:{key}", sid):
                leave_room(key)
                emit('message', {
                    'message': f"{user} has left Room {key}"}, room=key)

        # set named room_members:ASDF contains sid of users in the room
        r.sadd(f"room_members:{room}", sid)
        r.set(name=sid, value=user)  # key-value pair for sid and user name

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
    for key in list(r.smembers("set_of_rooms")):
        if r.srem(f"room_members:{key}", sid):  # check which room the user left
            emit('message', {
                 'message': f"{r.get(sid)} has left Room {key}"}, room=key)
            members = [r.get(member) for member in list(
                r.smembers(f"room_members:{key}"))]
            emit('update_room_members', {'room_occupants': members}, room=key)
    r.delete(sid)


@socketio.on("connect")
def connect():
    print(f"{request.sid} connected.\n\n\n\n")


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
    userSIDs = [member for member in list(r.smembers(f"room_members:{room}"))]
    userNames = [r.get(sid) for sid in userSIDs]
    userEnergies = [MAX_ENERGY for _ in userSIDs]
    scores = [0 for _ in userSIDs]
    playedThisTurn = [False for _ in userSIDs]
    turn = 0
    centerCards = []
    centerCardsPlayerIndex = []
    userCards = []
    lastRoundDesc = "Select a card to begin"
    totalNumberOfRounds = 1

    r.set(f"room_card_id:{room}", CARD_START_ID)

    cards = [r.hgetall(f"card:{key}")
             for key in list(r.smembers("card_index"))]

    for _ in userSIDs:
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
        "userSIDs": userSIDs,
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
