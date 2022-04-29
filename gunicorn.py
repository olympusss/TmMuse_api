# import multiprocessing
import os
from dotenv import load_dotenv
load_dotenv()


bind = "0.0.0.0:3000"

# workers = multiprocessing.cpu_count () * 2 + 1
# !!! socket isletmek un worker 1 bolmaly
workers = 1 
debug = os.environ.get("debug", "false") == "true"
keepalive = 120
timeout = 120
worker_class = "uvicorn.workers.UvicornWorker"
threads = 3
max_requests = 999999
reload = debug
backlog = 2048
worker_connections = 1024
limit_request_fields = 32768
limit_request_line = 8190
errorlog = '-'
accesslog = '-'