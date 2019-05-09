from flask import Flask, jsonify, request, abort
import json
import uuid
import datetime
import pandas as pd

app = Flask(__name__)

#crops = pd.read_csv('Production_Crops_E_Americas_manageable.csv', encoding='latin-1')

@app.route('/jobs', methods=['POST'])
def jobs_api():
    try:
        job = request.get_json(force=True)
    except Exception as e:
        return True, json.dumps({'status': "Error", 'message':'Invalid JSON: {}.', format(e)})
    return json.dumps(jobs.add_job(job['start', job['end']))

@app.route('/jobs/plot', methods=['GET'])
def make_plot():
    #an enpoint that makes a plot of the data

@app.route('/job_id/uuid')
def get_job_info():
    #returns all of the info for a certain job id

    # takes stuff from the url in the curl and puts it into a json (new_job) and puts the jobID in the queue
    
