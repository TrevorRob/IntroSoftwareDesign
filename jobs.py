import json, uuid, redis, Queue
from hotqueue import HotQueue

rd.redis.StrictRedis(host='172.17.0.1', port=6379, db=0)

q = HotQueue("queue", host='172,17.0.1', port=6379, db=1)

jl = redis.StrictRedis("job_log", host='172.17.0.1', port=6379, db=2)

#job.py
def generate_jid():
    return str(uuid.uuid4())

def generate_job_key(jid):
    return 'job.{}'.format(jid)

def instantiate_job(jid, status, start, end):
    if type(jid) == str:
        return {'id': jid,
                'status': status,
                'start': start,
                'end': end
        }
    return {'id': jid.decode('utf-8'),
            'status': status.decode('utf-8'),
            'start': start.decode('utf-8'),
            'end': end.decode('utf-8')
    }

def save_job(job_key, job_dict):
#    """Save a job object in the Redis database."""
    jl.hmset(job_key, json.dumps(job_dict))
        #the json.dumps might not be necessary
        #also what do we return here???

def queue_job(jid, job_dict):
#    """Add a job to the redis queue."""
    q.put(jid)
    job_dict['status']='pending'
    #what to return here??


def add_job(start, end, status="submitted"):
#    """Add a job to the redis queue."""
    jid = generate_jid()
    job_dict = instantiate_job(jid, status, start, end)
    job_key = generate_job_key(jid)
    save_job(job_key, job_dict)
    queue_job(jid, job_dict)
    return job_dict

def update_job_status(jid, status):
    """Update the status of job with job id `jid` to status `status`."""
    jid, status, start, end = jl.hmget(generate_job_key(jid), 'id', 'status', 'start', 'end')
    job = _instantiate_job(jid, status, start, end)
    if job:
        job['status'] = status
        _save_job(_generate_job_key(jid), job)
    else:
        raise Exception()

