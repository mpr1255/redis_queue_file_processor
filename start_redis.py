import redis
import os

r = redis.Redis(host='localhost', port=6379, db=0)
files = ["file1.txt", "file2.txt", "file3.txt"]

for file in files:
    if not r.sismember("processed_files", file):
        r.lpush("file_queue", file)
