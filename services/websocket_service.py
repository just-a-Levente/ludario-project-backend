from fastapi import WebSocket

class WebSocketManager:
    def __init__(self):
        self.__active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.__active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.__active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.__active_connections:
            await connection.send_json(message)

ws_manager = WebSocketManager()