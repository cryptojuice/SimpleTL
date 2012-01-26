from redis import Redis
import datetime
from ast import literal_eval

#Create connection to redis server
redis = Redis()

class Task(object):

    def __init__(self, note="Empty", completed=False, createdOn=str(datetime.date.today())):
        self.note = note
        self.completed = completed
        self.createdOn = createdOn

    # New task will contain the user_id who created it, a note, completed status, created datetime,
    # and a task_id
    def create_task(self, user_id, note):
        """ create_task(user_id, note) """

        task_id = redis.incr("task_id", 1)
        newTask = {'task_id':task_id, 'note':note, 'completed':self.completed,\
            'createdOn':self.createdOn} 
        redis.set("user:%s:task:%s" % (user_id, task_id), newTask)
        redis.sadd("task:lists", "user:%s:task:%s" % (user_id, task_id))
        return redis.get("user:%s:task:%s" % (user_id, task_id))
   

    def update_task(self, user_id, task_id, note, completed=False):
        pass
        return redis.get("user:%s:task:%s" % (user_id, task_id))

    def mark_complete(self, user_id, task_id):
        currentTask = redis.get("user:%s:task:%s" % (user_id, task_id))
        currentTask = literal_eval(currentTask)
        currentTask['completed'] = True
        redis.set("user:%s:task:%s" % (user_id, task_id), currentTask)
        return True

    def delete_task(self, user_id, task_id):
       pass 


    def display_all(self, user_id):
        temp_list = []
        user_tasks = []
        for item in redis.smembers("task:lists"):
            if ("user:%s" % user_id) in item:
                temp_list.append(item)
        
        for item in temp_list:
           user_tasks.append(literal_eval(redis.get(item))['createdOn'] + " " + \
               literal_eval(redis.get(item))['note'])
        return user_tasks
