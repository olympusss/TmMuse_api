import multiprocessing
import os
from dotenv import load_dotenv
load_dotenv()


bind = "0.0.0.0:3000"

worker_class = "uvicorn.workers.UvicornWorker"
workers = multiprocessing.cpu_count () * 2 + 1
debug = os.environ.get("debug", "false") == "true"
# max_requests = 5120
reload = debug
# preload_app = False
# daemon = False
backlog = 2048
worker_connections = 1024
timeout = 120
keepalive = 2
# spew = False
# pidfile = None
# umask = 0
# user = None
# group = None
# tmp_upload_dir = None

# def post_fork(server, worker):
#     server.log.info("Worker spawned (pid: %s)", worker.pid)

# def pre_fork(server, worker):
#     pass

# def pre_exec(server):
#     server.log.info("Forked child, re-executing.")

# def when_ready(server):
#     server.log.info("Server is ready. Spawning workers")

def worker_int(worker):
    worker.log.info("worker received INT or QUIT signal")
    import threading, sys, traceback
    id2name = {th.ident: th.name for th in threading.enumerate()}
    code = []
    for threadId, stack in sys._current_frames().items():
        code.append("\n# Thread: %s(%d)" % (id2name.get(threadId,""),
            threadId))
        for filename, lineno, name, line in traceback.extract_stack(stack):
            code.append('File: "%s", line %d, in %s' % (filename,
                lineno, name))
            if line:
                code.append("  %s" % (line.strip()))
    worker.log.debug("\n".join(code))
    worker.log.info("\n", code)
def worker_abort(worker):
    worker.log.info("worker received SIGABRT signal")