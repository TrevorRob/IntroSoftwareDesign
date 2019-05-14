import csv, redis, json
import sys

rd = redis.StrictRedis(host='172.17.0.1', port=6379, db=0)

def read_csv_data(csv_file, ik, iv):
    with open(csv_file, encoding='utf-8') as csvf:
        csv_data = csv.reader(csvf)
        return [(r[ik], r[iv]) for r in csv_data]

def store_data(conn, data):
    for i in data:
        conn.setnx(i[0], i[1])
    return data

def main():
    if len(sys.argv) < 2:
        sys.exit(
                "Usage: %s sunspots.csv [Year, Mean Daily Sunspots]"
                % __sunspots__
                )
    columns = (0, 1) if len(sys.argv) < 4 else(int(x) for x in sys.argv[2:4])
    data = read_csv_data(sys.argv[1], *columns)
    print (json.dumps(store_data(rd, data)))

