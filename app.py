from flask import Flask, jsonify, request, abort
import json
import uuid
import datetime
import pandas as pd

#Flask app
app = Flask(__name__)

#rd = redis.StrictRedis(host='172.17.0.1', port=6379, db=0)

jl = redis.StrictRedis("job_log", host='172.17.0.1', port=6379, db=2)

#data = json.load(open('crops_DS.json','r'))

def put_job_in_log(param, cmd):
    jobs.add_job(param, cmd)

#i think the methods on all of these may need to be 'PUT' instead

@app.route('/year/<int:year>', methods=['GET'])
def get_year_spots(year):
    param = {'year': year}
    cmd = "get_year()"
    put_job_in_log(param, cmd)
    #the year may need to be a string

@app.route('/max', methods=['GET'])
def get_max_spots():
    param = "want year of max sunpots"
    cmd = "get_max()"
    put_job_in_log(param, cmd)

@app.route('/min', methods=['GET'])
def get_min_spots():
    param = "want year of min sunpots"
    cmd = "get_min()"
    put_job_in_log(param, cmd)

@app.route('/jobs', methods=['POST'])
def jobs_api():
    try:
        job = request.get_json(force=True)
    except Exception as e:
        return True, json.dumps({'status': "Error", 'message':'Invalid JSON: {}.', format(e)})
    return json.dumps(jobs.add_job(job['start', job['end']))
#im not exactly sure what this is for and we may need to change it to at least fit the rest of the routes
# takes stuff from the url in the curl and puts it into a json (new_job) and puts the jobID in the queue

@app.route('/plot/<str:kind>', methods=['GET'])
def make_plot_years_spots(kind):
    param = {"type of plot": kind}
    cmd = "make_plot()"
    put_job_in_log(param, cmd)
#an enpoint that makes a plot of the data

@app.route('/job_id/<str:jid>', methods=['GET'])
def get_job_info(jid):
    timeL = []
    for key in jl:
        if key['id'] == jid:
            time = key['time stamp']
            timeL.append(time)
    recent = max(timeL)
    for key in jl:
        if key['time stamp'] == recent:
            return jsonify(jl.hmget(key))
#actually i just realized that all of this needs to be in the worker i think because it's just another job that the worker needs to pull off but I'm going to leave it here because I'm not exactly sure if that's right and even if it is I need to leave it so I can reproduce it later
#I have no idea if this will actually work but it seems like it could be right...?
#returns all of the info for a certain job id
