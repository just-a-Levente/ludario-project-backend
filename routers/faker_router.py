import asyncio
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from services.boardgame_service import boardgame_service
from services.faker_service import generate_fake_boardgame
from services.websocket_service import ws_manager

faker_router = APIRouter(prefix="/api/boardgames/faker", tags=["faker"])

faker_task: asyncio.Task | None = None

async def faker_loop():
    while True:
        create_request = generate_fake_boardgame()
        boardgame_service.create_boardgame(create_request)
        await ws_manager.broadcast({
            "event": "boardgame_added"
        })
        await asyncio.sleep(2)

@faker_router.get("/start", status_code=200)
async def start_faker():
    global faker_task
    if faker_task is None or faker_task.done():
        faker_task = asyncio.create_task(faker_loop())
    return { "status": "started" }

@faker_router.get("/stop", status_code=200)
async def stop_faker():
    global faker_task
    if faker_task and not faker_task.done():
        faker_task.cancel()
    return { "status": "stopped" }

@faker_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await ws_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)