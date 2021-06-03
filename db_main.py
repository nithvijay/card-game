import redis
import random
import json

# r = redis.Redis(host='localhost', port=6379, db=0) # for running locally
r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True) # for docker-compose
def pprint(data):
    print(json.dumps(data))

for key in r.keys():
    r.delete(key)

def initial_input(cards):
    for card in cards:
        r.hset(f"card:{card['text']}", mapping=card)
        r.sadd("card_index", card['text'])

cards = [
    {"text": "Sword", "attack": 3, "cost": 2},
    {"text": "Pistol", "attack": 5, "cost": 3},
    {"text": "Shotgun", "attack": 10, "cost": 5},
    {"text": "Knife", "attack": 1, "cost": 1},
]
initial_input(cards)


##################
### Game Logic ###
##################

def get_room_data(room):
    return json.loads(r.get(f"room_data:{room}"))

def set_room_data(room, room_data):
    r.set(f"room_data:{room}", json.dumps(room_data))

room = "QWER"
num_cards = 3

data = {"room":room, "num_cards":num_cards}
def start_game(data):
    room = data['room']
    num_cards = data['num_cards']

    sids = ["123", "456", "789"]
    for sid in sids:
        r.sadd(f"room_keys:{room}", sid)

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


start_game(data)

room_data = get_room_data(room)

###############
## play_card ##
###############

def play_card(room, sid, played_id):
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
            # emit something to let others know which card moved
            # emit('play_card_client', ) # send all info? or just what card changed?
    set_room_data(room, room_data)

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

### Simulation of Game

def one_step_simul(sid, id, msg="One step simmed!"): # as similar as possible to socket.io server event handler for "card-click"
    play_card(room, sid, id)
    room_data = get_room_data(room)
    winner = check_win(room_data)
    print(msg, winner)
    return winner

sid = "123"
winner = one_step_simul(sid=sid, id=room_data[sid]['cards'][0]['id'])
sid = "456"
winner = one_step_simul(sid=sid, id=room_data[sid]['cards'][0]['id'])
sid = "789"
winner = one_step_simul(sid=sid, id=room_data[sid]['cards'][0]['id'])

def emit_win(room, winner):
    room_data = get_room_data(room)
    room_data[winner['sid']]['score'] += 1 # increase winner's score
    room_data['playing_field'] = {'player_index': [], 'field': {}}
    set_room_data(room, room_data)

emit_win(room, winner)
room_data = get_room_data(room)
pprint(room_data)

sid = "123"
winner = one_step_simul(sid=sid, id=room_data[sid]['cards'][0]['id'])
sid = "456"
winner = one_step_simul(sid=sid, id=room_data[sid]['cards'][0]['id'])
sid = "789"
winner = one_step_simul(sid=sid, id=room_data[sid]['cards'][0]['id'])

emit_win(room, winner)
room_data = get_room_data(room)
pprint(room_data)

sid = "123"
winner = one_step_simul(sid=sid, id=room_data[sid]['cards'][0]['id'])
sid = "456"
winner = one_step_simul(sid=sid, id=room_data[sid]['cards'][0]['id'])
sid = "789"
winner = one_step_simul(sid=sid, id=room_data[sid]['cards'][0]['id'])

emit_win(room, winner)
room_data = get_room_data(room)
pprint(room_data)