from flask import Flask, jsonify, request, abort
import json
import uuid
import datetime

app = Flask(__name__)

# @app.route('/', methods=['POST'])

def generate_jobID():
    return str(uuid.uuid4())

def new_job(jobID, CMD, pm):
    time = str(datetime.datetime.now())
    return {'id': jobID,
            'status': 'new',
            'time': time,
            'command': CMD,
            'parameters': pm }
    
