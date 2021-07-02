import redis
import os

from db_init import initial_input

def reset_db():
    REDIS_ADDRESS = os.getenv('REDIS_ADDRESS', 'redis')
    r = redis.Redis(host=REDIS_ADDRESS, port=6379, db=0, decode_responses=True)

    for key in r.keys():
        r.delete(key)
    
    initial_input(r)

if __name__ == "__main__":
    reset_db()
