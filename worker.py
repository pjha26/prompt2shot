import os
import sys

# Make sure our app modules can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rq import SimpleWorker, Queue
from app.queue import redis_conn

listen = ['default']

if __name__ == '__main__':
    print("Starting RQ worker...")
    queues = [Queue(name, connection=redis_conn) for name in listen]
    # SimpleWorker is required on Windows (no os.fork support).
    # It executes jobs in the same process without forking.
    worker = SimpleWorker(queues, connection=redis_conn)
    worker.work()
