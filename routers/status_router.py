from fastapi import APIRouter, status

status_router = APIRouter(prefix="/api/status", tags=["status"])

@status_router.get("/", status_code=status.HTTP_200_OK)
def get_connection_status():
    return {"status": "ok"}