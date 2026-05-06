from fastapi import APIRouter, status
from schemas.api_schema import ReviewDisplayResponse, ReviewCreateRequest
from services.review_service import review_service

review_router = APIRouter(prefix="/api/reviews", tags=["reviews"])

@review_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=ReviewDisplayResponse
)
def create_review(request: ReviewCreateRequest):
    return review_service.create_review(request)

@review_router.delete(
    "/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_review(review_id: int):
    review_service.delete_review(review_id)