from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from websocket import manager
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
import uvicorn

app = FastAPI()


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
app.include_router(interest_router         , tags=["Interest"])
app.include_router(home_router             , tags=["Home"])
app.include_router(profile_router          , tags=["Profile"])
app.include_router(category_router         , tags=["Category"])
app.include_router(answers_router          , tags=["Answer"])
app.include_router(card_router             , tags=["Card"])
app.include_router(constant_router         , tags=["Constant"])
app.include_router(search_router           , tags=["Search"])
app.include_router(ticket_router           , tags=["Ticket"])

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket</h1>
        <button onClick="showForm(event)" id="connect">Connect</button>
        <form action="" onsubmit="sendMessage(event)" id="form" style="display: none">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var clientID = Date.now();
            var ws = new WebSocket(`ws://10.192.168.16:8000/ws`);

            function processMessage(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content);
                messages.appendChild(message);
            }

            ws.onmessage = processMessage;

            function sendMessage(event) {
                var input = document.getElementById("messageText")
                var message = document.createElement('li')
                var content = document.createTextNode(input.value)
                message.appendChild(content);
                messages.appendChild(message);
                ws.send(input.value);

                input.value = ''
                event.preventDefault()
            }

            function showForm(event) {
                var button = document.getElementById("connect");
                var form = document.getElementById("form");
                button.style.display = "none";
                form.style.display = "block";
            }

        </script>
    </body>
</html>
"""

@app.get("/")
async def html_response():
    return HTMLResponse(html)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    while True:
        data = await websocket.receive_text()
        await manager.broadcast(f"Client: {data}")
        
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)