import main
from typing import Any
import socketio

sio: Any = socketio.AsyncServer(cors_allowed_origins='*', async_mode="asgi")
socket_app = socketio.ASGIApp(sio)

@sio.on("connect")
async def connect(sid, env):
    print("on connect")
    
    
@sio.on("direct")
async def direct(sid, msg):
    print(f"direct {msg}")
    await sio.emit("event_name", msg, room=sid)
    
    
@sio.on("onMessage")
async def broadcast(sid, msg):
    print(f"onMessage {msg}")
    await sio.emit("onMessage", msg)
    
    
    
@sio.on("disconnect")
async def disconnect(sid):
    print("on disconnect")