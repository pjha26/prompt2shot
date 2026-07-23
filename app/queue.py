import redis
from rq import Queue
from app.config import settings

# Initialize Redis connection
redis_conn = redis.from_url(settings.REDIS_URL, protocol=2)

# Initialize RQ Queue
# We'll use the default queue for generation tasks
generation_queue = Queue("default", connection=redis_conn)
