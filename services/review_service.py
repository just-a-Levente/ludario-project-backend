from model.review import Review
from schemas.api_schema import *
from repository.review_repository import ReviewRepository
from schemas.review_api_mapper import ReviewAPIMapper

class ReviewService:

    def __init__(self):
        self.__repository = ReviewRepository()

    def get_reviews_for_boardgame(self, boardgame_id: int) -> list[Review]:
        return self.__repository.get_reviews_for_boardgame(boardgame_id)

    def get_review(self, review_id: int) -> Review | None:
        return self.__repository.get_review(review_id)

    def create_review(self, create_request: ReviewCreateRequest) -> ReviewDisplayResponse:
        review_instance = ReviewAPIMapper.create_review_from_request(create_request)
        self.__repository.insert_review(review_instance)
        return ReviewAPIMapper.review_to_display_response(review_instance)

    def delete_review(self, review_id: int) -> None:
        self.__repository.delete_review(review_id)

    def delete_reviews_for_boardgame(self, boardgame_id: int) -> None:
        reviews_to_delete = self.__repository.get_reviews_for_boardgame(boardgame_id)
        for review in reviews_to_delete:
            self.__repository.delete_review(review.id)

    def update_review(self, update_request: ReviewUpdateRequest) -> Review:
        review_instance = ReviewAPIMapper.update_review_from_request(update_request)
        self.__repository.update_review(review_instance)
        return review_instance

review_service = ReviewService()