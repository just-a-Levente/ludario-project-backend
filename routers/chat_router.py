import pymongo
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from services.chat_websocket_service import chat_ws_manager
from db import messages_collection
from datetime import datetime, timezone

chat_router = APIRouter(prefix="/api/chat", tags=["chat"])

@chat_router.get("/history")
async def get_chat_history(limit: int = 50):
    cursor = messages_collection.find(
        {},
        {"_id": 0}
    ).sort("timestamp", pymongo.DESCENDING).limit(limit)

    messages = await cursor.to_list(length=limit)
    return list(reversed(messages))

@chat_router.websocket("/ws/{email}")
async def chat_websocket(websocket: WebSocket, email: str):
    await chat_ws_manager.connect(email, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            message = {
                "sender": email,
                "content": data["content"],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
            await messages_collection.insert_one({**message})
            await chat_ws_manager.broadcast(message)
    except WebSocketDisconnect:
        chat_ws_manager.disconnect(email)
        await chat_ws_manager.broadcast({
            "sender": "system",
            "content": f"{email} left the chat",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        })