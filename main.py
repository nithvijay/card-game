from flask import Flask, redirect, render_template, url_for, request
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import datetime

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home(): # Users type the chat room they want to go to
    if request.method == 'POST':
        room = request.form['room']
        return redirect(url_for('rooms', room=room))
    else:
        return render_template('index.html')

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
    username = data['username']
    room = data['room']
    join_room(room)
    emit('chat message', {'message': f"{username} has entered Room {room}"}, room=room)

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
    emit('chat message', {'message': f"{datetime.datetime.now(tz=datetime.timezone(datetime.timedelta(hours=-5))).strftime('%I:%M:%S %p')} - {username}: {message}"}, room=room)

# @socketio.on('connect')
# def please_work():
#     print("Someone connected")

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