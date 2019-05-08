import redis
import json
import hotqueue
from hotqueue import HotQueue

rd = redis.StrictRedis(host='172,17.0.1', port=6379, db=0)

q = HotQueue("queue", host='172.17.0.1', port=6379 db=1)

jl = redis.StrictRedis("job_log", host='172.17.0.1', port=6379, db=2)

stat = [ 'pending' , 'in progress'. 'complete' ]

def update_status(jobID):
    #query database to get keyID of most recent log in jl
    #using the json of the keyID, find the status
    key['status'] = stat[+1]
    #I really don't think that's right but it's what I want to happen

