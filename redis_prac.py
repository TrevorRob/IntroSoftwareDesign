import csv, redis, json
import sys

rd = redis.StrictRedis(host='172.17.0.1', port=6379, db=0)

def read_csv_data(csv_file, ik, iv
