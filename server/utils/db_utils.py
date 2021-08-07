import datetime


def gen_random_pid(db):
    new_pid = str(
        hash(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S.%f")))
    db.sadd('set_of_pids', new_pid)
    return new_pid


def clear_database(db):
    for key in db.keys():
        db.delete(key)


CARDS = [
    {
        "name": "Apple",
        'value': 3,
        'type': 'Goods'
    },
    {
        "name": "Cheese",
        'value': 5,
        'type': 'Goods'
    },
    {
        "name": "Hammers",
        'value': 7,
        'type': 'Contraband'
    },
    {
        "name": "Gems",
        'value': 9,
        'type': 'Contraband'
    },
]
