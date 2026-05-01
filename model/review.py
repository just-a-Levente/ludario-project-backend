from datetime import date, datetime

from pydantic import BaseModel

class Review(BaseModel):
    id: int = -1
    boardgame_id: int = -1
    author: str = "unknown"
    stars: int = 0
    comment: str = ""
    review_date: date = datetime.date(datetime.now())