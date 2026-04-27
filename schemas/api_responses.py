from pydantic import BaseModel

class BoardgameBase(BaseModel):
    name:               str
    producer:           str
    description:        str
    price:              float
    numberOfCopies:     int
    minNumberOfPlayers: int
    maxNumberOfPlayers: int
    thumbnailURL:       str
    tags:               str

class BoardgameCreateRequest(BoardgameBase):
    pass

class BoardgameUpdateRequest(BoardgameBase):
    id: int

class BoardgameDeleteRequest(BaseModel):
    id: int


class BoardgameDisplayResponse(BaseModel):
    id:                 int
    name:               str
    producer:           str
    description:        str
    price:              float
    numberOfCopies:     int
    minNumberOfPlayers: int
    maxNumberOfPlayers: int
    thumbnailURL:       str
    tags:               list[str]