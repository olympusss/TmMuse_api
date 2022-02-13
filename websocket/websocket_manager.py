from typing import List
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.connections.append(websocket)

    async def broadcast(self, data: str):
        for connection in self.connections:
            try:
                await connection.send_text(data)
            except Exception as e:
                print("Error: ", e)
                continue
        print(data)

manager = ConnectionManager()