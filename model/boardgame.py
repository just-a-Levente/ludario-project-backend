from pydantic import BaseModel

class Boardgame(BaseModel):
    id: int
    hidden: bool = False
    name: str = ""
    producer: str = ""
    description: str = ""
    price: float = 0
    numberOfCopies: int = 0
    minNumberOfPlayers: int = 1
    maxNumberOfPlayers: int = 1
    thumbnailURL: str = ""
    tags: list[str] = []
    stars: list[int] = []