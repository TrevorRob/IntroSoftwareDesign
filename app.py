from flask import Flask, jsonify, request, abort
import json
import uuid
import datetime

app = Flask(__name__)

@app.route('/jobs', methods=['POST'])
def jobs_api():
    try:
        job = request.get_json(force=True)
    except Exception as e:
        return True, json.dumps({'status': "Error", 'message':'Invalid JSON: {}.', format(e)})
    return json.dumps(jobs.add_job(job['start', job['end']))


    # takes stuff from the url in the curl and puts it into a json (new_job) and puts the jobID in the queue
    
