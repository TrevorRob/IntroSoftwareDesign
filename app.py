from flask import Flask, jsonify, request, abort
import csv, json, uuid, datetime
import sys
import pandas as pd

#Flask app
app = Flask(__app__)

rd = redis.StrictRedis(host='172.17.0.1', port=6379, db=0)

jl = redis.StrictRedis("job_log", host='172.17.0.1', port=6379, db=2)

def read_csv_data(csv_file, ik, iv):
    with open(csv_file, encoding='utf-8') as csvf:
        csv_data = csv.reader(csvf)
        return [(r[ik], r[iv]) for r in csv_data]

def store_data(conn, data):
    for i in data:
        rd.setnx(i[0], i[1])
    return data

def data_function():
    if len(sys.argv) < 2:
    sys.exit(
        "Usage: %s sunspots.csv [Year, Mean Daily Sunspots]"
        % __sunspots__
    )
    columns = (0,1) if len(sys.argv) < 4 else (int(x) for x in sys.argv([2:4])
    data = read_csv_data(sys.argv[1], *columns)
#    return (json.dumps(store_data(rd, data)))

def put_job_in_log(param, cmd):
    jobs.add_job(param, cmd)

#returns all the data
@app.route('/')
def sunspots():
    return jsonify(rd)

#i think the methods on all of these may need to be 'PUT' instead

@app.route('/year/<int:year>', methods=['GET'])
def get_year_spots(year):
#     param = {'year': year}
#    cmd = "get_year()"
#    put_job_in_log(param, cmd)
    return jsonify(rd.hget(year))

@app.route('/max', methods=['GET'])
def get_max_spots():
#    param = "want year of max sunpots"
#    cmd = "get_max()"
#    put_job_in_log(param, cmd)
    mean = []
    for year in rd:
        mean.append(rd.hget())
    return max(mean)


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
    return json.dumps(jobs.add_job(job['start'], job['end']))
            
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
