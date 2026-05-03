import datetime

from model.review import Review

class ReviewRepository:

    def __init__(self):
        self.__reviews: dict[int, Review] = {}
        self.__lastID: int = 0
        self.__add_examples()

    def __add_examples(self):
        self.insert_review(Review(
            id=-1,
            boardgame_id=1,
            author="Admin",
            stars=3,
            comment="this board game is meh",
            review_date=datetime.date(2026, 5, 1)
        ))
        self.insert_review(Review(
            id=-1,
            boardgame_id=1,
            author="Admin",
            stars=4,
            comment="this board game is good",
            review_date=datetime.date(2026, 5, 3)
        ))

    def reset_repo(self):
        self.__reviews = {}
        self.__lastID = 0

    @property
    def all_reviews(self) -> list[Review]:
        return list(self.__reviews.values())

    @property
    def number_of_reviews(self) -> int:
        return len(self.__reviews)

    def __increment_last_id(self):
        self.__lastID += 1

    def get_review(self, review_id: int) -> Review | None:
        return self.__reviews.get(review_id)

    def get_reviews_for_boardgame(self, boardgame_id: int) -> list[Review]:
        reviews_for_boardgame = []
        for review in self.all_reviews:
            if review.boardgame_id == boardgame_id:
                reviews_for_boardgame.append(review)
        return reviews_for_boardgame

    def insert_review(self, new_review: Review):
        if new_review.id == -1:
            new_id = self.__lastID
            self.__increment_last_id()
            new_review.id = new_id
        self.__reviews[new_review.id] = new_review

    def update_review(self, updated_review: Review):
        self.__reviews[updated_review.id] = updated_review

    def delete_review(self, review_id_to_delete: int):
        self.__reviews.pop(review_id_to_delete)