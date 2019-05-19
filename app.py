from flask import Flask, jsonify, request, abort
import csv, json, uuid, datetime
import sys
import pandas as pd
import redis
from jobs import add_job 
import os 

REDIS_IP = os.environ.get('REDIS_IP')
REDIS_PORT  = os.environ.get('REDIS_PORT')
#Flask app
app = Flask(__name__)

rd = redis.StrictRedis(host='172.17.0.1', port=6379, db=0)

jl = redis.StrictRedis(host='172.17.0.1', port=6379, db=2)

def put_job_in_log(param, cmd):
    job_dict = add_job(param, cmd)
    return job_dict['id']

#returns all the data
@app.route('/')
def sunspots():
    param = "want all the sunspot data"
    cmd = "data"
    jobID = put_job_in_log(param, cmd)
    return jobID
#    return jsonify(rd)

#i think the methods on all of these may need to be 'PUT' instead

@app.route('/year', methods=['POST'])
def post_year():
    request_data = request.json
    param = request_data
    cmd = "post_new_data"
    put_job_in_log(param,cmd)
    jobID = put_job_in_log(param, cmd)
    return jobID


@app.route('/year/<int:year>', methods=['GET'])
def get_year_spots(year):
    param = {'year': year}
    cmd = "year_spots"
    jobID = put_job_in_log(param, cmd)
    return jobID
#    return jsonify(rd.hget(year))

@app.route('/max', methods=['GET'])
def get_max_spots():
    param = "want year of max sunspots"
    cmd = "max"
    jobID = put_job_in_log(param, cmd)
    return jobID
#    mean = []
#    for year in rd:
#        mean.append(rd.hget())
#    return max(mean)


@app.route('/min', methods=['GET'])
def get_min_spots():
    param = "want year of min sunspots"
    cmd = "min"
    jobID = put_job_in_log(param, cmd)
    return jobID
#@app.route('/jobs', methods=['POST'])
#def jobs_api():
#    try:
#        job = request.get_json(force=True)
#    except Exception as e:
#        return True, json.dumps({'status': "Error", 'message':'Invalid JSON: {}.', format(e)})
#    return json.dumps(jobs.add_job(job['start'], job['end']))
            
            #im not exactly sure what this is for and we may need to change it to at least fit the rest of the routes
# takes stuff from the url in the curl and puts it into a json (new_job) and puts the jobID in the queue

@app.route('/plot/<string:kind>', methods=['GET'])
def make_plot_years_spots(kind):
    param = {"type of plot": kind}
    cmd = "plot"
    jobID = put_job_in_log(param, cmd)
    return jobID

@app.route('/job_id/<string:jid>', methods=['GET'])
def get_job_info(jid):
    timeL = []
    for key in jl:
        if key['id'] == jid:
            time = key['time stamp']
            timeL.append(time)
    recent = max(timeL)
    for key in jl:
        if key['id'] == id and key['time stamp'] == recent:
            job_info = json.loads(jl.hgetall(key).decode('utf-8'))
            #return jsonify(jl.hmget(key))
            return job_info
