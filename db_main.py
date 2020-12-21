import redis

# r = redis.Redis(host='localhost', port=6379, db=0) # for running locally
r = redis.Redis(host='redis', port=6379, db=0) # for docker-compose

# r.lpush("test1", "1", "2", "3")
# print(r.lrange('test1', 0, 5))
# print(r.keys())
# print(r.delete("test1"))
# print(r.keys())

# print("\n\nNEW")
# r.set("some_user_sid", "room1234")
# print(r.get("some_user_sid"))
# r.set("some_user_sid", "newroom12345")
# print(r.get("some_user_sid"))
# print(r.keys())
# print(r.delete("some_user_sid"))
# print(f"Not present user: {r.get('some_user_sid')}")
# print(r.keys())


# room key
room1 = "room1"
room2 = "room2"
user1 = "user1"
user2 = "user2"
user3 = "user3"
user4 = "user4"
user5 = "user5"

# r.sadd("list_of_rooms", room1)
# r.sadd(f"room_keys:{room1}", user1)
# r.sadd("list_of_rooms", room1)
# r.sadd(f"room_keys:{room1}", user2)

# r.sadd("list_of_rooms", room2)
# r.sadd(f"room_keys:{room2}", user3)
# r.sadd("list_of_rooms", room2)
# r.sadd(f"room_keys:{room2}", user4)
# r.sadd("list_of_rooms", room2)
# r.sadd(f"room_keys:{room2}", user5)

# print(r.smembers("list_of_rooms"))
# print(r.smembers("list_of_rooms"))

for key in r.keys():
    r.delete(key)
    

def add_key(user, room):
    r.sadd(f"list_of_rooms", room)
    for key in r.scan_iter("room_keys:*"): # so users can only be part of one room, potentially slow with large number of rooms
        if r.srem(key, user):
            print(f"Removed {user} from {key}")
    r.sadd(f"room_keys:{room}", user)

add_key(user1, room1)
add_key(user2, room2)
add_key(user3, room1)
add_key(user4, room1)
add_key(user5, room2)
add_key(user3, room2)
add_key(user4, room2)
add_key(user2, room1)

for key in r.scan_iter("room_keys:*"):
    print(key, r.smembers(key))


r.lpush("test1", "1", "2", "3")
print(r.exists("test1"))
print(r.exists("test2"))

print(r.lrange("test1", 0, 20))
print(r.lrange("test2", 0, 20))

for key in r.keys():
    r.delete(key)