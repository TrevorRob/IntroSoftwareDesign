import redis
import json
import hotqueue
import csv
from hotqueue import HotQueue
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from jobs import update_job_status, current_time, generate_job_key, save_job 
from app import get_job_info
import os
import seaborn as sns
import sys


REDIS_IP = os.environ.get('REDIS_IP')
REDIS_PORT  = os.environ.get('REDIS_PORT')
#worker

rd = redis.StrictRedis(host=REDIS_IP, port=REDIS_PORT, db=0)

q = HotQueue("queue", host=REDIS_IP, port=REDIS_PORT, db=1)

jl = redis.StrictRedis("job_log", host=REDIS_IP, port=REDIS_PORT, db=2)

plots = redis.StrictRedis("plots", host=REDIS_IP, port=REDIS_PORT, db=3)

daily_spots = pd.read_csv('sunspots.csv')
daily_spots.columns = ['Year', 'Mean Daily Spots']
daily_spots = daily_spots.set_index('Year')

@q.worker
def execute_job(jid):
# add stuff here
    jobs.update_job_status(jid,"running")
    job = app.get_job_info(jid)
    command=job["command"]
    param = job["param"]
    if command == "plot":
        kind = param['type of plot']
        if kind == 'histogram' or kind == 'line' kind == 'scatter':
            makePlot(jid, kind)
            save_plot_to_redis(jid)

        else:
            jobs.update_job_status(jid, 'failed')
    elif command == "year_spots":
        year = param['year']
        if year in range(1770, 1869):
            result = year_spots(year)   
            save_job_result(jid, result)
        else:
            jobs.update_job_status(jid, 'failed')
    elif command == "max":
        result = get_max()
        save_job_result(jid, result)
    elif command == "min":
        result = get_min()
        save_job_result(jid, result)
    elif command == "post_new_data":
        year = param['Year']
        spots = param['Mean Daily Spots']
        if len(param) != 4:
            jobs.update_job_status(jid, "failed")
        elif year in range(1770,1869) or year < 0 or year > 2019: 
            jobs.update_job_status(jid, 'failed')
        elif spots < 0:
            jobs.update_job_status(jid, 'failed')
        else:
            result = post_new_data(param)
            save_job_result(jid, result)
    elif command == "data":
        result = get_data()
        save_job_result(jid, result)

def save_job_result(jid, result):
    key = jobs.generate_job_key(jid)
    time = jobs.current_time()
    job_dict = {'id': jid,
                'status': 'complete',
                'time stamp': time,
                'result': result}
    jobs.save_job(key, job_dict)

def post_new_data(param):
    year = param['Year']
    mean = param['Mean Daily Spots']
    new = pd.DataFrame({'Year': [year], 'Mean Daily Spots': [mean]})
    new = new.set_index('Year')
    daily_spots = daily_spots.append(new)
    return daily_spots

def year_spots(year)
    return daily_spots['Mean Daily Spots'].loc[year]

def get_max()
    year = daily_spots['Mean Daily Spots'].idxmax()
    spots = daily_spots['Mean Daily Spots'].max()
    return {'Year of Max Sunspots': year, 'Number of Max Sunspots': spots}

def get_min()
    year = daily_spots['Mean Daily Spots'].idxmin()
    spots = daily_spots['Mean Daily Spots'].min()
    return {'Year of Min Sunspots': year, 'Number of Min Sunspots': spots}
    
def get_data()
    return daily_spots

def save_plot_to_redis(key):
    file_bytes = open('/tmp/scatter_plot.png', 'rb').read()
    plots.set(key, file_bytes)
    save_job_result(jid,file_bytes)

def makePlot(jid, plot):
#    x = daily_spots['Year']
#    y = daily_spots['Mean Daily Spots']
    if plot == "histogram":
        sns.set(rc={'figure.figsize':(11,4)})
        ax = daily_spots['Mean Daily Sunspots'].plot(kind='hist',title='Histogram of Mean Daily Sunspots Frequency')
        ax.set_xlabel("Mean Daily Sunspots")
        plt.savefig('/tmp/histogram.png', dpi=150)
        file_bytes = open('/tmp/histogram.png', 'rb').read()
        save_job_result(jid, file_bytes)

    if plot == "scatter":
        plt.scatter(x,y)
        plt.set_xlabel("Year")
        plt.set_ylabel("Mean Daily Sunpots")
        plt.show()
    if plot == "line":
        #ax = daily_spots['Mean Daily Spots'].plot()
        plt.plot(x,y)
        plt.set_xlabel("Year")
        plt.set_ylabel("Mean Daily Sunpots")
        plt.show()
        sns.set(rc={'figure.figsize':(11,4)})
        daily_spots['Mean Daily Sunspots'].plot(marker='.', linestyle='None')
        #plt.set_xlabel("Year")
        ax.set_ylabel("Mean Daily Sunpots")
        plt.savefig('/tmp/scatter_plot.png', dpi=150)
        file_bytes = open('/tmp/scatter_plot.png', 'rb').read()
        save_job_result(jid, file_bytes)

    if plot == "line":
        #ax = daily_spots['Mean Daily Spots'].plot()
        #plt.plot(x,y)
        sns.set(rc={'figure.figsize':(11,4)})
        daily_spots['Mean Daily Sunspots'].plot(linewidth=2.0)
        ax.set_ylabel("Mean Daily Sunpots")
        plt.savefig('/tmp/line_plot.png', dpi=150)
        file_bytes = open('/tmp/line_plot.png', 'rb').read()
        save_job_result(jid, file_bytes)
       # plt.set_xlabel("Year")
       # plt.set_ylabel("Mean Daily Sunpots")
       # plt.savefig('/tmp/line_plot.png', dpi=150)
        #update_job_status?
    else
        jobs.update_job_status(jid, "failed")

