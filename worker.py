import os
from rq import Worker, Queue, Connection
from app.queue import redis_conn

# Make sure our app modules can be imported
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

listen = ['default']

if __name__ == '__main__':
    print("Starting RQ worker...")
    with Connection(redis_conn):
        worker = Worker(map(Queue, listen))
        worker.work()
