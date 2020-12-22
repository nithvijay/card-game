import datetime

import eventlet
from flask import Flask, redirect, render_template, request, url_for, jsonify, session
from flask_socketio import SocketIO, emit, join_room, leave_room, send
import redis

eventlet.monkey_patch()


app = Flask(__name__)
socketio = SocketIO(app, message_queue="redis://redis:6379", async_handlers=True, async_mode='eventlet')
r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True)


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
            members = [r.get(member) for member in list(r.smembers(key))]
            context.append(dict(
                key=key,
                members=members, #sets do not work nicely with iteration
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
    r.sadd(f"list_of_rooms", room) # set named list_of_rooms contains all rooms 
    for key in r.scan_iter("room_keys:*"): # so users can only be part of one room, potentially slow with large number of rooms
        if r.srem(key, sid):
            old_room = key.split(":")[1]
            leave_room(old_room)
            emit('chat message', {'message': f"{user} has left Room {old_room}"}, room=old_room)

    
    r.sadd(f"room_keys:{room}", sid) # set named room_keys:ASDF contains sid of users in the room
    r.set(name=sid, value=user) #key-value pair for sid and user name

    emit('message_history', {'message_history': r.lrange(room, 0, 1000)})
    emit('chat message', {'message': f"{user} has entered Room {room}"}, room=room)
    members = [r.get(member) for member in list(r.smembers(f"room_keys:{room}"))]
    emit('update_room', {'room_occupants': members}, room=room)

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
    r.lpush(room, to_send)

    emit('debug', {'sid': request.sid, 'session': session.get('room')})
    emit('chat message', {'message': to_send}, room=room)

@socketio.on('disconnect')
def on_disconnect():
    sid = request.sid
    for key in r.scan_iter("room_keys:*"): #check which room the user left
        if r.srem(key, sid):
            room = key.split(":")[1]
            emit('chat message', {'message': f"{r.get(sid)} has left Room {room}"}, room=room)
            members = [r.get(member) for member in list(r.smembers(f"room_keys:{room}"))]
            emit('update_room', {'room_occupants': members}, room=room)
    r.delete(sid)

@socketio.on('delete history')
def delete_history(data):
    room = data['room']
    r.delete(room)

# @socketio.on('disconnecting')
# def on_disconnect():
#     emit('chat message', {'message': "someone is leaving, but hasn't left yet"}, broadcast=True)


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
