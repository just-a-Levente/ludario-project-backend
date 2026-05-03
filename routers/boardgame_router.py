from fastapi import APIRouter, status, Query
from services.boardgame_service import boardgame_service
from services.review_service import review_service
from schemas.review_api_mapper import ReviewAPIMapper
from schemas.boardgame_api_mapper import BoardgameAPIMapper
from schemas.api_schema import *

boardgame_router = APIRouter(prefix="/api/boardgames", tags=["boardgames"])

@boardgame_router.get("/")
def get_all_boardgames():
    return boardgame_service.get_all_boardgames()

@boardgame_router.get(
    "/page",
    response_model=PaginatedBoardgamesResponse
)
def get_boardgames(offset: int = Query(0, ge=0), limit: int = Query(10, ge=1, le=50)):
    return boardgame_service.get_boardgames(offset, limit)

@boardgame_router.get(
    "/{boardgame_id}",
    response_model=BoardgameDetailResponse
)
def get_boardgame(boardgame_id: int):
    boardgame_details = boardgame_service.get_boardgame(boardgame_id)
    reviews_of_boardgame = review_service.get_reviews_for_boardgame(boardgame_id)
    review_displays = [ReviewAPIMapper.review_to_display_response(review) for review in reviews_of_boardgame]
    return BoardgameAPIMapper.boardgame_and_reviews_to_detail_response(boardgame_details, review_displays)

@boardgame_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=BoardgameDisplayResponse
)
def create_boardgame(request: BoardgameCreateRequest):
    return boardgame_service.create_boardgame(request)

@boardgame_router.delete(
    "/{boardgame_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_boardgame(boardgame_id: int):
    boardgame_service.delete_boardgame(boardgame_id)

@boardgame_router.put(
    "/",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=BoardgameDisplayResponse
)
def update_boardgame(request: BoardgameUpdateRequest):
    return boardgame_service.update_boardgame(request)


# --------
# Reviews
# --------

@boardgame_router.post(
    "/reviews",
    status_code=status.HTTP_201_ACCEPTED,
    response_model=ReviewDisplayResponse
)
def create_review(request: ReviewCreateRequest):
    return review_service.create_review(request)

@boardgame_router.delete(
    "/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_review(review_id: int):
    review_service.delete_review(review_id)