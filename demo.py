from fastapi import FastAPI
from fastapi_socketio import SocketManager

app = FastAPI()

sio = SocketManager(app=app, cors_allowed_origins=["*"])

@app.get("/")
def read_root():
    return {"Hello": "World"}

@sio.on('connect')
async def connect():
    print('connect')

if __name__ == '__main__':
    import logging
    import sys

    logging.basicConfig(level=logging.DEBUG,
                        stream=sys.stdout)

    import uvicorn

    uvicorn.run("main:app", host='127.0.0.1',
                port=8000, reload=True, debug=False)