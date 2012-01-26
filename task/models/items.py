#item has a title, note, id, creation date.
from redis import Redis
from datetime import datetime

redis = Redis()


def create_item(title, note):
    id = redis.incr("item_id", 1)
    redis.set("item:%s:title" % (id), title)
    redis.set("item:%s:note" % (id), note)
    redis.set("item:%s:created_on" % (id), datetime.now())
    return True
    
