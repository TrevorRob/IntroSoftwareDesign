import redis
import json
import hotqueue
from hotqueue import HotQueue

rd = redis.StrictRedis(host='172,17.0.1', port=6379, db=0)

#q = HotQueue("queue", host='172.17.0.1', port=6379 db=1)

#jl = redis.StrictRedis("job_log", host='172.17.0.1', port=6379, db=2)

@q.worker
def execute_job(jid):
# add stuff here

