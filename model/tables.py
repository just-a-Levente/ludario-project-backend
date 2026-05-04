from datetime import date
from sqlalchemy import Integer, String, Float, Boolean, Date, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class BoardgameTagORM(Base):
    __tablename__ = "boardgame_tags"

    id           : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    boardgame_id : Mapped[int] = mapped_column(ForeignKey("boardgames.id"))
    tag          : Mapped[str]

class BoardgameORM(Base):
    __tablename__ = "boardgames"

    id                 : Mapped[int]  = mapped_column(primary_key=True, autoincrement=True)
    hidden             : Mapped[bool] = mapped_column(default=False)
    name               : Mapped[str]
    producer           : Mapped[str]
    description        : Mapped[str]
    price              : Mapped[float]
    numberOfCopies     : Mapped[int]
    minNumberOfPlayers : Mapped[int]
    maxNumberOfPlayers : Mapped[int]
    thumbnailURL       : Mapped[str]
    tags               : Mapped[list["BoardgameTagORM"]] = relationship(cascade="all, delete-orphan")
    reviews            : Mapped[list["ReviewORM"]]       = relationship(back_populates="boardgame", cascade="all, "
                                                                                                            "delete-orphan")

class ReviewORM(Base):
    __tablename__ = "reviews"

    id           : Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    boardgame_id : Mapped[int] = mapped_column(ForeignKey("boardgames.id"))
    author       : Mapped[str]
    stars        : Mapped[int]
    comment      : Mapped[str]
    review_date  : Mapped[date]
    boardgame    : Mapped["BoardgameORM"] = relationship(back_populates="reviews")