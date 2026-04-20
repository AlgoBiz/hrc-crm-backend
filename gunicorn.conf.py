# Gunicorn configuration for HRC CRM Backend
# Path: /var/www/hrc-crm-backend/gunicorn.conf.py

import multiprocessing

# Server socket
bind = "127.0.0.1:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 120
keepalive = 5

# Restart workers after this many requests (prevents memory leaks)
max_requests = 1000
max_requests_jitter = 100

# Logging
accesslog = "/var/www/hrc-crm-backend/logs/gunicorn_access.log"
errorlog  = "/var/www/hrc-crm-backend/logs/gunicorn_error.log"
loglevel  = "warning"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "hrc_crm"

# Server mechanics
daemon = False
pidfile = "/var/www/hrc-crm-backend/gunicorn.pid"
user = "www-data"
group = "www-data"
tmp_upload_dir = None

# SSL (handled by Nginx, not needed here)
forwarded_allow_ips = "127.0.0.1"
