from flask import Flask, jsonify, request, abort
import json
import uuid
import datetime

app = Flask(__name__)

# @app.route('/', methods=['POST'])
    # takes stuff from the url in the curl and puts it into a json (new_job) and puts the jobID in the queue

def generate_jobID():
    return str(uuid.uuid4())

def generate_job_key(jobID):
    return 'job.{}'.format(jobID)

# status = [ 'pending', 'in progress', 'complete' ]

def new_job(jobID, CMD, pm):
    time = str(datetime.datetime.now())
    return {'id': jobID,
            'status': 'new',
            'time': time,
            'command': CMD,
            'parameters': pm }
    
