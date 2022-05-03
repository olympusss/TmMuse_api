from fastapi import FastAPI
from starlette.responses import HTMLResponse
from starlette.websockets import WebSocket, WebSocketDisconnect
from typing import List
from db import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from routers import authentication_router
from routers import interest_router
from routers import home_router
from routers import profile_router
from routers import category_router
from routers import answers_router
from routers import card_router
from routers import constant_router
from routers import search_router
from routers import ticket_router
from routers import view_count_router
from routers import users_router

app = FastAPI(
    title='TmMuse Mobile API'
)

origins = ["*"]
methods = ["*"]
headers = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=methods,
    allow_headers=headers,
)


Base.metadata.create_all(engine)
app.include_router(authentication_router   , tags=["Authentication"])
app.include_router(users_router            , tags=["Users"])
app.include_router(interest_router         , tags=["Interest"])
app.include_router(home_router             , tags=["Home"])
app.include_router(profile_router          , tags=["Profile"])
app.include_router(category_router         , tags=["Category"])
app.include_router(answers_router          , tags=["Answer"])
app.include_router(card_router             , tags=["Card"])
app.include_router(constant_router         , tags=["Constant"])
app.include_router(search_router           , tags=["Search"])
app.include_router(ticket_router           , tags=["Ticket"])
app.include_router(view_count_router       , tags=["Click_View"])

    
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://95.85.125.22:3000/ws");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/websocket", tags=["Websocket"])
async def get():
    return HTMLResponse(html)


class Notifier:
    def __init__(self):
        self.connections: List[WebSocket] = []
        self.generator = self.get_notification_generator()

    async def get_notification_generator(self):
        while True:
            message = yield
            await self._notify(message)

    async def push(self, msg: str):
        await self.generator.asend(msg)

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    def remove(self, websocket: WebSocket):
        self.connections.remove(websocket)

    async def _notify(self, message: str):
        living_connections = []
        while len(self.connections) > 0:
            # Looping like this is necessary in case a disconnection is handled
            # during await websocket.send_text(message)
            websocket = self.connections.pop()
            await websocket.send_text(message)
            living_connections.append(websocket)
        self.connections = living_connections


notifier = Notifier()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await notifier.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        notifier.remove(websocket)


@app.get("/push/{message}", tags=["Websocket"])
async def push_to_connected_websockets(message: str):
    await notifier.push(f"! Push notification: {message} !")


@app.on_event("startup")
async def startup():
    # Prime the push notification generator
    await notifier.generator.asend(None)