def initial_input(r):
    cards = [
        {"text": "Sword", "attack": 3, "cost": 3},
        {"text": "Pistol", "attack": 5, "cost": 5},
        {"text": "Shotgun", "attack": 10, "cost": 7},
        {"text": "Knife", "attack": 1, "cost": 1},
    ]
    for card in cards:
        r.hset(f"card:{card['text']}", mapping=card)
        # r.hmset(f"card:{card['text']}", ("text", card['text']), ('attack', card['attack']), ('cost', card['cost']))
        r.sadd("card_index", card['text'])

    MAIN_ID_START = 1
    r.set("main_id_generator", MAIN_ID_START)