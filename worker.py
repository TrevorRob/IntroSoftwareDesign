import redis
import json
import hotqueue
from hotqueue import HotQueue
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#worker

rd = redis.StrictRedis(host='172,17.0.1', port=6379, db=0)

q = HotQueue("queue", host='172.17.0.1', port=6379, db=1)

jl = redis.StrictRedis("job_log", host='172.17.0.1', port=6379, db=2)

@q.worker
def execute_job(jid):
# add stuff here
    jobs.update_job_status(jid,running)
    rd.get()


