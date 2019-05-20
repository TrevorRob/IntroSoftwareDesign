import json, uuid, redis
import datetime
from datetime import timedelta
from hotqueue import HotQueue
import os 
from flask import jsonify

REDIS_IP = os.environ.get('REDIS_IP')
REDIS_PORT  = os.environ.get('REDIS_PORT')
#def get_redis_ip():
    #return os.environ.get('REDIS_IP')
    #host=get_redis_ip()

rd = redis.StrictRedis(host=REDIS_IP, port=REDIS_PORT, db=0)

q = HotQueue("queue", host=REDIS_IP, port=REDIS_PORT, db=1)

jl = redis.StrictRedis(host=REDIS_IP, port=REDIS_PORT, db=2)

def generate_jid():
    return str(uuid.uuid4())

def current_time():
    #d = timedelta(hours = -5)
    #tx = datetime.timezone(d)
    return str(datetime.datetime.now())

def generate_job_key(jid):
    return 'job.{}'.format(jid)

def instantiate_job(jid, status, param, cmd):
    time = current_time()
    if type(jid) == str:
        job_dict = json.dumps({'id': jid,
                'status': status,
                'time stamp': time,
                'parameters': param,
                'command': cmd
                })
    else:
        job_dict = json.dumps({'id': jid.decode('utf-8'),
                'status': status.decode('utf-8'),
                'time stamp': time.decode('utf-8'),
                'parameters': param.decode('utf-8'),
                'command': cmd.decode('utf-8')

                })
    return job_dict

def convert_job_fields(key):
    return { 'id': jl.hget(key, 'id').decode('utf-8'),
             'status': jl.hget(key, 'status').decode('utf-8'),
             'time stamp': jl.hget(key, 'time stamp').decode('utf-8'),
             'parameters': jl.hget(key, 'parameters').decode('utf-8'),
             'command': jl.hget(key, 'command').decode('utf-8') }

def save_job(job_key, job_dict):
#   jl.hmset(job_key, json.dumps(job_dict))
    jl.hmset(job_key, job_dict)

def queue_job(jid):
    q.put(jid)
    status = 'pending'
    update_job_status(jid, status)


def add_job(param, cmd, status="new"):
#    """Add a job to the redis queue."""
    jid = generate_jid()
    job_dict = instantiate_job(jid, status, param, cmd)
    job_key = generate_job_key(jid)
    save_job(job_key, job_dict)
    #job_dict = convert_job_fields(job_key)
    queue_job(jid)
    return job_dict

def update_job_status(jid, status):
    jid, status, param, cmd = jl.hmget(generate_job_key(jid), 'id', 'status', 'parameters', 'command')
    job = instantiate_job(jid, status, param, cmd)
    if job:
        job['status'] = status
        save_job(generate_job_key(jid), job)
    else:
        raise Exception()

