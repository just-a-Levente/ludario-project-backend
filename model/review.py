from datetime import date

from pydantic import BaseModel

class Review(BaseModel):
    id: int
    boardgameId: int
    author: str = "unknown"
    stars: int = 0
    comment: str = ""
    reviewDate: date