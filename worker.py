import os
import sys
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# Make sure our app modules can be imported
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rq import SimpleWorker, Queue
from app.queue import redis_conn

listen = ['default']

class DummyHandler(BaseHTTPRequestHandler):
    """
    This HTTP server exists only to satisfy Render's free-tier Web Service 
    port requirement. It serves no real purpose in the application logic.
    """
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"OK")
        
    def log_message(self, format, *args):
        # Suppress logging to keep the worker logs clean
        pass

def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    server_address = ("0.0.0.0", port)
    httpd = HTTPServer(server_address, DummyHandler)
    print(f"Starting dummy HTTP server on port {port} for Render health checks...")
    httpd.serve_forever()

if __name__ == '__main__':
    # Start the dummy HTTP server in a background thread
    server_thread = threading.Thread(target=run_dummy_server, daemon=True)
    server_thread.start()

    print("Starting RQ worker...")
    queues = [Queue(name, connection=redis_conn) for name in listen]
    # SimpleWorker is required on Windows (no os.fork support).
    # It executes jobs in the same process without forking.
    worker = SimpleWorker(queues, connection=redis_conn)
    worker.work()
