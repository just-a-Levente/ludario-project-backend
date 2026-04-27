from model.boardgame import Boardgame
from api_schema import *

class BoardgameAPIMapper:

    @staticmethod
    def create_boardgame_from_request(request: BoardgameCreateRequest) -> Boardgame:
        return Boardgame(
            id=-1,
            name=request.name,
            producer=request.producer,
            description=request.description,
            price=float(request.price),
            numberOfCopies=int(request.numberOfCopies),
            minNumberOfPlayers=int(request.minNumberOfPlayers),
            maxNumberOfPlayers=int(request.maxNumberOfPlayers),
            thumbnailURL=request.thumbnailURL,
            tags=request.tags.split(';')
        )

    @staticmethod
    def update_boardgame_from_request(request: BoardgameUpdateRequest) -> Boardgame:
        return Boardgame(
            id=request.id,
            name=request.name,
            producer=request.producer,
            description=request.description,
            price=float(request.price),
            numberOfCopies=int(request.numberOfCopies),
            minNumberOfPlayers=int(request.minNumberOfPlayers),
            maxNumberOfPlayers=int(request.maxNumberOfPlayers),
            thumbnailURL=request.thumbnailURL,
            tags=request.tags.split(';')
        )

    @staticmethod
    def boardgame_to_display_response(boardgame: Boardgame) -> BoardgameDisplayResponse:
        return BoardgameDisplayResponse(
            id=boardgame.id,
            name=boardgame.name,
            producer=boardgame.producer,
            description=boardgame.description,
            price=boardgame.price,
            numberOfCopies=boardgame.numberOfCopies,
            minNumberOfPlayers=boardgame.minNumberOfPlayers,
            maxNumberOfPlayers=boardgame.maxNumberOfPlayers,
            thumbnailURL=boardgame.thumbnailURL,
            tags=boardgame.tags
        )