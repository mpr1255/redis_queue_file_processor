import redis
import os

r = redis.Redis(host='localhost', port=6379, db=0)
files = os.list.dir('take_an_argument here')

for file in files:
    if not r.sismember("processed_files", file):
        r.lpush("file_queue", file)
