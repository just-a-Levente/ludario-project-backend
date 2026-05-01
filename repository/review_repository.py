from model.review import Review

class ReviewRepository:

    def __init__(self):
        self.__reviews: dict[int, Review] = {}
        self.__lastID: int = 0

    def reset_repo(self):
        self.__reviews = {}
        self.__lastID = 0

    @property
    def all_reviews(self) -> list[Review]:
        return list(self.__reviews.values())

    @property
    def number_of_reviews(self) -> int:
        return len(self.__reviews)

    @property
    def last_review_id(self) -> int:
        return self.__lastID

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
            new_id = self.last_review_id
            self.__increment_last_id()
            new_review.id = new_id
        self.__reviews[new_review.id] = new_review

    def update_review(self, updated_review: Review):
        self.__reviews[updated_review.id] = updated_review

    def delete_review(self, review_id_to_delete: int):
        self.__reviews.pop(review_id_to_delete)