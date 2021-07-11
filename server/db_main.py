import json

import redis

from database_wrapper import DB
from utils.db_init import init_database
from utils.db_utils import gen_random_pid

r = redis.Redis(host='redis', port=6379, db=0,
                decode_responses=True)  # for docker-compose
db = DB(r)


def pprint(data):
    print(json.dumps(data))


for key in db.keys():
    db.delete(key)
