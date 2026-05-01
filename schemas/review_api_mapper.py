import datetime

from model.review import Review
from api_schema import *

class ReviewAPIMapper:

    @staticmethod
    def create_review_from_request(request: ReviewCreateRequest) -> Review:
        return Review(
            id=-1,
            boardgame_id=request.boardgame_id,
            author=request.author,
            stars=request.stars,
            comment=request.comment,
            review_date=datetime.date.fromisoformat(request.review_date),
        )

    @staticmethod
    def update_review_from_request(request: ReviewUpdateRequest) -> Review:
        return Review(
            id=request.id,
            boardgame_id=request.boardgame_id,
            author=request.author,
            stars=request.stars,
            comment=request.comment,
            review_date=datetime.date.fromisoformat(request.review_date),
        )

    @staticmethod
    def review_to_display_response(review: Review) -> ReviewDisplayResponse:
        return ReviewDisplayResponse(
            id=review.id,
            boardgame_id=review.boardgame_id,
            author=review.author,
            stars=review.stars,
            comment=review.comment,
            review_date=datetime.date.isoformat(review.review_date),
        )