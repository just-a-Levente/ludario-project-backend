from sqlalchemy import Column, Integer, String, Float, Boolean, Date, ForeignKey
from sqlalchemy.orm import DeclarativeBase, relationship

class Base(DeclarativeBase):
    pass

class BoardgameORM(Base):
    __tablename__ = "boardgames"
    id                 = Column(Integer, primary_key=True, autoincrement=True)
    hidden             = Column(Boolean, default=False)
    name               = Column(String)
    producer           = Column(String)
    description        = Column(String)
    price              = Column(Float)
    numberOfCopies     = Column(Integer)
    minNumberOfPlayers = Column(Integer)
    maxNumberOfPlayers = Column(Integer)
    thumbnailURL       = Column(String)
    tags               = Column(String)  # stored as semicolon-separated string
    reviews            = relationship("ReviewORM", back_populates="boardgame", cascade="all, delete")

class ReviewORM(Base):
    __tablename__ = "reviews"
    id           = Column(Integer, primary_key=True, autoincrement=True)
    boardgame_id = Column(Integer, ForeignKey("boardgames.id"))
    author       = Column(String)
    stars        = Column(Integer)
    comment      = Column(String)
    review_date  = Column(Date)
    boardgame    = relationship("BoardgameORM", back_populates="reviews")