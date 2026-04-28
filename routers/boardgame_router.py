from fastapi import APIRouter, HTTPException, status
from services.boardgame_service import boardgame_service
from schemas.api_schema import BoardgameDisplayResponse, BoardgameCreateRequest, BoardgameUpdateRequest

boardgame_router = APIRouter(prefix="/api/boardgames", tags=["boardgames"])

@boardgame_router.get(
    "/"
)
def get_all_boardgames():
    return boardgame_service.get_all_boardgames()

@boardgame_router.get(
    "/{boardgame_id}",
    response_model=BoardgameDisplayResponse
)
def get_boardgame(boardgame_id: int):
    boardgame = boardgame_service.get_boardgame(boardgame_id)
    return boardgame

@boardgame_router.post(
    "/",
    status_code=status.HTTP_201_CREATED
)
def create_boardgame(request: BoardgameCreateRequest):
    boardgame_service.create_boardgame(request)

@boardgame_router.delete(
    "/{boardgame_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_boardgame(boardgame_id: int):
    boardgame_service.delete_boardgame(boardgame_id)

@boardgame_router.put(
    "/",
    status_code=status.HTTP_204_NO_CONTENT
)
def update_boardgame(request: BoardgameUpdateRequest):
    boardgame_service.update_boardgame(request)