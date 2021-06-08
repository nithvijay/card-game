import datetime
import json
import random

import eventlet
import redis
from flask import Flask, request
from flask_socketio import SocketIO, emit, join_room, leave_room, send

eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", message_queue="redis://redis:6379", async_handlers=True, async_mode='eventlet')
r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)


def initial_input(cards):
    for card in cards:
        r.hset(f"card:{card['text']}", mapping=card)
        # r.hmset(f"card:{card['text']}", ("text", card['text']), ('attack', card['attack']), ('cost', card['cost']))
        r.sadd("card_index", card['text'])


cards = [
    {"text": "Sword", "attack": 3, "cost": 2},
    {"text": "Pistol", "attack": 5, "cost": 3},
    {"text": "Shotgun", "attack": 10, "cost": 5},
    {"text": "Knife", "attack": 1, "cost": 1},
]

initial_input(cards)


@socketio.on('join')
def on_join(data):  # This is called in chatapp.js when the user submits a name in /rooms/<room>
    user = data['username']
    room = data['room']
    sid = request.sid
    join_room(room)

    # index of keys
    r.sadd("set_of_rooms", room)  # set named set_of_rooms contains all rooms
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
    emit('message', {'message': f"{user} has entered Room {room}"}, room=room)
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

    # emit('debug', {'sid': request.sid, 'session': session.get('room')})
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


################
## Game Logic ##
################
CARD_START_ID = 0


def get_room_data(room):
    return json.loads(r.get(f"roomData:{room}"))


def set_room_data(room, roomData):
    r.set(f"roomData:{room}", json.dumps(roomData))


@socketio.on('start_game')
def start_game(room):
    emit("game_started", "", room=room)
    roomData = dict()
    userSIDs = [member for member in list(r.smembers(f"room_members:{room}"))]
    userNames = [r.get(sid) for sid in userSIDs]
    scores = [0 for _ in userSIDs]
    turn = 0
    centerCards = []
    userCards = []

    r.set(f"room_card_id:{room}", CARD_START_ID)

    cards = [r.hgetall(f"card:{key}")
             for key in list(r.smembers("card_index"))]

    for _ in userSIDs:
        rand_cards = random.choices(cards, k=3)
        player_cards = []
        for card in rand_cards:
            card_id = r.get(f"room_card_id:{room}")
            r.set(f"room_card_id:{room}", int(card_id) + 1)
            card['id'] = card_id
            player_cards.append(card.copy())
        userCards.append(player_cards)

    roomData = {
        "userCards": userCards,
        "centerCards": centerCards,
        "userNames": userNames,  # ordered
        "userSIDs": userSIDs,
        "scores": scores,
        "turn": turn
    }
    set_room_data(room, roomData)
    emit("update_game_state", roomData, room=room)


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')
