from starlette.websockets import WebSocket
from typing import List

from app.db.redis_connection import redis_previous_device_data


class WebSocketConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket, subscribe_id: str):
        await websocket.accept()
        self.active_connections.append(websocket)

        r = redis_previous_device_data
        p = r.pubsub()
        p.subscribe(subscribe_id)
        return p

    def disconnect(self, websocket: WebSocket, pubsub, client_id):
        self.active_connections.remove(websocket)
        pubsub.unsubscribe(client_id)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)