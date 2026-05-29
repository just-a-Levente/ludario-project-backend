from fastapi import APIRouter, status, Depends
from schemas.api_schema import ReviewDisplayResponse, ReviewCreateRequest
from services.review_service import review_service
from utils.token_functions import require_permission

review_router = APIRouter(prefix="/api/reviews", tags=["reviews"])

@review_router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ReviewDisplayResponse
)
def create_review(request: ReviewCreateRequest, _ = Depends(require_permission("create_review"))):
    return review_service.create_review(request)

@review_router.delete(
    "/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_review(review_id: int, _ = Depends(require_permission("delete_review"))):
    review_service.delete_review(review_id)

# TODO: add PUT (update) to reviews