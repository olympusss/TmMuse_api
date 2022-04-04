import multiprocessing
import os
from dotenv import load_dotenv
load_dotenv()


bind = "0.0.0.0:3000"

worker_class = "uvicorn.workers.UvicornWorker"
workers = multiprocessing.cpu_count () * 2 + 1
debug = os.environ.get("debug", "false") == "true"
max_requests = 999999
reload = debug
backlog = 2048
worker_connections = 1024
timeout = 30
keepalive = 2
limit_request_fields = 32768
limit_request_line = 8190
errorlog = '-'
accesslog = '-'


