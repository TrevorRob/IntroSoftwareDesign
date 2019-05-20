from flask import Flask, jsonify, request, abort
import csv, json, uuid, datetime
#import sys
#import pandas as pd
import redis
from jobs import add_job 
import os 
import pandas as pd
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib as plt

#import seaborn as sns
#import sys

REDIS_IP = os.environ.get('REDIS_IP')
REDIS_PORT  = os.environ.get('REDIS_PORT')
#Flask app
app = Flask(__name__)

rd = redis.StrictRedis(host=REDIS_IP, port=REDIS_PORT, db=0)

jl = redis.StrictRedis(host=REDIS_IP, port=REDIS_PORT, db=2)

plots = redis.StrictRedis(host=REDIS_IP, port=REDIS_PORT, db=3)

daily_spots = pd.read_csv('sunspots.csv')
daily_spots.columns = ['Year', 'Mean Daily Spots']
daily_spots = daily_spots.set_index('Year')

@app.route('/')
def sunspots():
    return jsonify(daily_spots)

@app.route('/year', methods=['POST'])
def post_year():
    year = request.args.get('year')
    mean = request.args.get('spots')
    new = pd.DataFrame({'Year': [year], 'Mean Daily Spots': [mean]})
    new = new.set_index('Year')
    daily_spots = daily_spots.append(new)
    return jsonify(daily_spots)


@app.route('/year/<string:year>', methods=['GET'])
def get_year_spots(year):
    return jsonify(daily_spots['Mean Daily Spots'].loc[int(year)])

@app.route('/max', methods=['GET'])
def get_max_spots():
    year = daily_spots['Mean Daily Spots'].idxmax()
    spots = daily_spots['Mean Daily Spots'].max()
    return jsonify({'Year of Max Sunspots': year, 'Number of Max Sunspots': spots})

@app.route('/min', methods=['GET'])
def get_min_spots():
    year = daily_spots['Mean Daily Spots'].idxmin()
    spots = daily_spots['Mean Daily Spots'].min()
    return jsonify({'Year of Min Sunpots': year, 'Number of Min Sunpots': spots})

@app.route('/plot/<string:kind>', methods=['GET'])
def make_plot_years_spots(kind):
    if kind == 'histogram':
        #sns.set(rc={'figure.figsize':(11,4)})
        ax = daily_spots['Mean Daily Spots'].plot(kind='hist',title='Histogram of Mean Daily Sunspots Frequency')
        ax.set_xlabel("Mean Daily Sunspots")
        fig = ax.get_figure()
        fig.savefig('spots_histogram.png')
        result = "The plot has been saved in the current directory as spots_histogram.png"
        return result
    elif kind == 'scatter':
        #sns.set(rc={'figure.figsize':(11,4)})
        ax = daily_spots['Mean Daily Spots'].plot(marker='.', linestyle='None')
        ax.set_ylabel("Mean Daily Sunspots")
        fig = ax.get_figure()
        fig.savefig('spots_scatter.png')
        result = "The plot has been saved in the current directory as spots_scatter.png"
        return result
    elif kind == 'line':
        #sns.set(rc={'figure.figsize':(11,4)})
        ax = daily_spots['Mean Daily Spots'].plot(linewidth=2.0)
        ax.set_ylabel("Mean Daily Sunspots")
        fig = ax.get_figure()
        fig.savefig('spots_line.png')
        retult = "The plot has been saved in the current directory as spots_line.png"
        return result








