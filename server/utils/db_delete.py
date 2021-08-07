import redis
import os
from database_wrapper import DB
from db_utils import clear_database


if __name__ == "__main__":
    REDIS_ADDRESS = os.getenv('REDIS_ADDRESS', 'localhost')
    r = redis.Redis(host=REDIS_ADDRESS, port=6379, db=0, decode_responses=True)
    db = DB(r)
    clear_database(db)
