import json


class DB:
    """Useful if switching away from Redis
    """

    def __init__(self, r) -> None:
        self.r = r

    def get(self, key):
        return self.r.get(key)

    def set(self, key, value):
        return self.r.set(key, value)

    def sadd(self, key, value):
        return self.r.sadd(key, value)

    def smembers(self, key):
        return self.r.smembers(key)

    def srem(self, key, value):
        return self.r.srem(key, value)

    def sismember(self, key, member):
        if member:
            return self.r.sismember(key, member)
        else:
            return False

    def keys(self):
        return self.r.keys()

    def delete(self, key):
        return self.r.delete(key)

    def exists(self, key):
        return bool(self.r.exists(key))

    def set_json(self, key, value):
        to_set = json.dumps(value)
        return self.set(key, to_set)

    def get_json(self, key):
        to_ret = self.get(key)
        return json.loads(to_ret)
