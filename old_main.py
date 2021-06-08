import datetime
import random

import eventlet
from flask import Flask, redirect, render_template, request, url_for, jsonify, session
from flask_socketio import SocketIO, emit, join_room, leave_room, send
import redis
import json

eventlet.monkey_patch()

app = Flask(__name__)
socketio = SocketIO(app, message_queue="redis://redis:6379", async_handlers=True, async_mode='eventlet')
r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)
card_start_id = 0

def get_room_data(room):
    return json.loads(r.get(f"room_data:{room}"))

def set_room_data(room, room_data):
    r.set(f"room_data:{room}", json.dumps(room_data))

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

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home(): # Users type the chat room they want to go to
    if request.method == 'POST':
        room = request.form['room']
        return redirect(url_for('rooms', room=room))
    else:
        context = []
        for key in r.scan_iter("room_keys:*"):
            room = key.split(":")[1]
            members = [r.get(member) for member in list(r.smembers(key))] #sets do not work nicely with iteration
            context.append(dict(
                key=key,
                members=members, 
                size=r.scard(key),
                peak=list(r.lrange(room, 0, 10))
            ))
        return render_template('index.html', rooms=context)

    

@app.route('/rooms/<room>')
def rooms(room): #the chat room itself. The URL is what determines the chat room. Therefore, it is possible to bypass the home page entirely
    return render_template('rooms.html', room=room)

@app.route('/chat')
def chat(): # Random template/testing page. Can be ignored
    return render_template('chat.html')

@app.route('/form', methods=['GET', 'POST'])
def form(): # Random page testing forms and javascript in flask. Can be ignored
    context = {}
    if request.method == 'POST':
        context['name'] = request.form['name']
    return render_template('form.html', context=context)

##################################
#### Socket.io event handlers ####
##################################

@socketio.on('join')
def on_join(data): # This is called in chatapp.js when the user submits a name in /rooms/<room>
    user = data['username']
    room = data['room']
    sid = request.sid
    join_room(room)

    # index of keys
    r.sadd("set_of_rooms", room) # set named set_of_rooms contains all rooms
    for key in list(r.smembers("set_of_rooms")): # so users can only be part of one room, potentially slow with large number of rooms, looping through all rooms to see 
        if r.srem(f"room_keys:{key}", sid):
            leave_room(key)
            emit('chat message', {'message': f"{user} has left Room {key}"}, room=key)
    
    r.sadd(f"room_keys:{room}", sid) # set named room_keys:ASDF contains sid of users in the room
    r.set(name=sid, value=user) #key-value pair for sid and user name

    # emit('message_history', {'message_history': r.lrange(f"room_message_history:{room}", 0, 1000)})
    emit('message', {'message': f"{user} has entered Room {room}"}, room=room)
    members = [r.get(member) for member in list(r.smembers(f"room_keys:{room}"))]
    # emit('update_room', {'room_occupants': members}, room=room)

@socketio.on('leave')
def on_leave(data): # not sure when/if this is called; needs more research
    username = data['username']
    room = data['room']
    leave_room(room)
    emit('chat message', {'message': f"{username} has left Room {room}"}, room=room)

@socketio.on("chat")
def handle_chat(data): #This is called in chatapp.js when the user sends a message to the room
    room = data['room']
    username = data['username']
    message = data['text']
    to_send = f"{datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=-5))).strftime('%I:%M:%S %p')} - {username}: {message}"
    r.lpush(f"room_message_history:{room}", to_send)

    emit('chat message', {'message': to_send}, room=room)

def check_win(room_data): #doesn't modify room_data
    if len(room_data['playing_field']['player_index']) == 3: # everyone has played a card
        # pprint(room_data['playing_field']['field'])
        temp = []
        for key in room_data['playing_field']['player_index']:
            temp.append({'sid':key, "attack": room_data['playing_field']['field'][key]['attack'], 'id': room_data['playing_field']['field'][key]['id']})
            # print(key, room_data['playing_field']['field'][key])
        # print(sorted(temp, key=lambda card: -int(card['attack']))) #first card in list will be the highest value
        winner = sorted(temp, key=lambda card: -int(card['attack']))[0]
        return winner
    return False

@socketio.on("start_game")
def start_game(data):
    num_cards = data['num_cards']
    room = data['room']
    # the server should keep the values of everyone's cards    
    card_start_id = 0
    r.set(f"room_card_id:{room}", card_start_id)

    cards = [r.hgetall(f"card:{key}") for key in list(r.smembers("card_index"))]
    
    room_data = dict()
    for member in list(r.smembers(f"room_keys:{room}")): #returns the sid of the player
        rand_cards = random.choices(cards, k=num_cards)
        player_cards = []
        for card in rand_cards:
            card_id = r.get(f"room_card_id:{room}")
            r.set(f"room_card_id:{room}", int(card_id) + 1)
            card['id'] = card_id
            player_cards.append(card.copy())
        room_data[member] = {'cards': player_cards, 'score': 0}
    
    room_data['playing_field'] = {'player_index': [], 'field': {}}
    set_room_data(room, room_data)
    emit('game_started', {'data': room_data, 'sid': request.sid}, room=room)


@socketio.on("play-card")
def play_card(data):
    room = data['room']
    sid = request.sid
    played_id = data['played_id']
    room_data = get_room_data(room)
    for card in room_data[sid]['cards']:
        if card['id'] == played_id:
            room_data['playing_field']['field'][sid] = card
            room_data['playing_field']['player_index'].append(sid)
            room_data[sid]['cards'].remove(card)

            key = r.srandmember("card_index")
            rand_card = r.hgetall(f"card:{key}")

            card_id = r.get(f"room_card_id:{room}")
            r.set(f"room_card_id:{room}", int(card_id) + 1)
            rand_card['id'] = card_id

            room_data[sid]['cards'].append(rand_card)
            emit('someone-played-card', {'room_data':room_data})

    set_room_data(room, room_data)
    winner = check_win(room_data)
    if winner:
        room_data[winner['sid']]['score'] += 1 # increase winner's score
        room_data['playing_field'] = {'player_index': [], 'field': {}}
        set_room_data(room, room_data)
        emit('someone-played-card', {'room_data':room_data})
    

@socketio.on('disconnect')
def on_disconnect():
    sid = request.sid
    for key in list(r.smembers("set_of_rooms")): #check which room the user left
        if r.srem(f"room_keys:{key}", sid):
            emit('chat message', {'message': f"{r.get(sid)} has left Room {key}"}, room=key)
            members = [r.get(member) for member in list(r.smembers(f"room_keys:{key}"))]
            emit('update_room', {'room_occupants': members}, room=key)
    r.delete(sid)

@socketio.on('delete history')
def delete_history(data):
    for key in r.keys():
        r.delete(key)
    cards = [
        {"text": "Sword", "attack": 3, "cost": 2},
        {"text": "Pistol", "attack": 5, "cost": 3},
        {"text": "Shotgun", "attack": 10, "cost": 5},
        {"text": "Knife", "attack": 1, "cost": 1},
    ]
    initial_input(cards)


@socketio.on('connect')
def connect():
    emit('sid', request.sid)


# @socketio.on('message')
# def handle_message(message):
#     send(f"You said: {message}")

# @socketio.on('json')
# def handle_json(json):
#     send(json, json=True)

# @socketio.on('my event')
# def handle_my_custom_event(json):
#     send("hello!")

if __name__ == "__main__":
    socketio.run(app, debug=True, host='0.0.0.0')
