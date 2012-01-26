from redis import Redis
from hashlib import md5

redis = Redis()

def create_user(email, password):
    if redis.sadd("users", email):
        id = redis.incr("user_id", 1)
        passhash = md5(password).hexdigest()
        redis.set("user:%s" % (id), "{'id':'%s', 'email':'%s', 'password':'%s'}" % \
                (id, email, passhash))
        redis.hset("users:lookup:email", email, id)
        redis.hset("users:lookup:password", id, passhash)
        return True
    return False

def delete_user(email):
    id = redis.hget("users:lookup:email", email)
    if redis.sismember("users", email):
        redis.delete("user:%s" % (id))
        redis.srem("users", email)
        redis.hdel("users:lookup:email", email)
        redis.hdel("users:lookup:password", id)
        return True
    return False

def authenticate_user(email, password):
    id = redis.hget("users:lookup:email", email)
    passhash = md5(password).hexdigest()
    if redis.sismember("users", email):
        user_password = redis.hget("users:lookup:password", id)
        if user_password == passhash:
            return True
    return False
