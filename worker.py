import os
from rq import Worker, Queue
from app.queue import redis_conn

# Make sure our app modules can be imported
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

listen = ['default']

if __name__ == '__main__':
    print("Starting RQ worker...")
    from rq import SimpleWorker
    queues = [Queue(name, connection=redis_conn) for name in listen]
    worker = SimpleWorker(queues, connection=redis_conn)
    worker.work()
