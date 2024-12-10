# Gunicorn configuration file for release mode
import multiprocessing
import os

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
threads = 2
worker_class = 'gthread'
worker_tmp_dir = '/dev/shm'

# Timeouts
timeout = 120
keepalive = 5

# Logging
errorlog = '-'
accesslog = '-'
loglevel = 'info'

# Process naming
proc_name = 'ska_release'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None

# Server hooks
def on_starting(server):
    """Log that the server is starting."""
    server.log.info("Starting release server...")

def on_reload(server):
    """Log that the server is reloading."""
    server.log.info("Reloading release server...")

def on_exit(server):
    """Log that the server is shutting down."""
    server.log.info("Shutting down release server...")

# Limits
max_requests = 1000
max_requests_jitter = 50

# Security
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190 