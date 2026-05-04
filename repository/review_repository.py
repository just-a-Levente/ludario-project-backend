import datetime
from sqlalchemy import func
from model.review import Review
from model.tables import ReviewORM
from db import SessionLocal

class ReviewRepository:

    def __init__(self):
        self.__add_examples()

    def __add_examples(self):
        if self.number_of_reviews > 0:
            return
        self.insert_review(Review(
            boardgame_id=1,
            author="Admin",
            stars=3,
            comment="this board game is meh",
            review_date=datetime.date(2026, 5, 1)
        ))
        self.insert_review(Review(
            boardgame_id=1,
            author="Admin",
            stars=4,
            comment="this board game is good",
            review_date=datetime.date(2026, 5, 3)
        ))

    def __to_model(self, orm: ReviewORM) -> Review:
        return Review(
            id=orm.id,
            boardgame_id=orm.boardgame_id,
            author=orm.author,
            stars=orm.stars,
            comment=orm.comment,
            review_date=orm.review_date,
        )

    @property
    def all_reviews(self) -> list[Review]:
        with SessionLocal() as session:
            orms = session.query(ReviewORM).all()
            return [self.__to_model(orm) for orm in orms]

    @property
    def number_of_reviews(self) -> int:
        with SessionLocal() as session:
            return session.query(func.count(ReviewORM.id)).scalar()

    def get_review(self, review_id: int) -> Review | None:
        with SessionLocal() as session:
            orm = session.get(ReviewORM, review_id)
            return self.__to_model(orm) if orm else None

    def get_reviews_for_boardgame(self, boardgame_id: int) -> list[Review]:
        with SessionLocal() as session:
            orms = session.query(ReviewORM).filter(
                ReviewORM.boardgame_id == boardgame_id
            ).all()
            return [self.__to_model(orm) for orm in orms]

    def insert_review(self, new_review: Review):
        with SessionLocal() as session:
            orm = ReviewORM(
                boardgame_id=new_review.boardgame_id,
                author=new_review.author,
                stars=new_review.stars,
                comment=new_review.comment,
                review_date=new_review.review_date,
            )
            session.add(orm)
            session.commit()
            session.refresh(orm)
            new_review.id = orm.id
            return new_review

    def update_review(self, updated_review: Review):
        with SessionLocal() as session:
            orm = session.get(ReviewORM, updated_review.id)
            if orm is None:
                return updated_review
            orm.author = updated_review.author
            orm.stars = updated_review.stars
            orm.comment = updated_review.comment
            orm.review_date = updated_review.review_date
            session.commit()
            return updated_review

    def delete_review(self, review_id_to_delete: int):
        with SessionLocal() as session:
            orm = session.get(ReviewORM, review_id_to_delete)
            if orm:
                session.delete(orm)
                session.commit()