from fastapi import WebSocket

class ChatWebsocketService:
    def __init__(self):
        self.__active_connections: dict[str, WebSocket] = {}

    async def connect(self, email: str, websocket: WebSocket):
        await websocket.accept()
        self.__active_connections[email] = websocket

    def disconnect(self, email: str):
        self.__active_connections.pop(email, None)

    async def broadcast(self, message: dict):
        for websocket in self.__active_connections.values():
            await websocket.send_json(message)

chat_ws_manager = ChatWebsocketService()