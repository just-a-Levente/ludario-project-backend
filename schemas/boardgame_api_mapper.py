from model.boardgame import Boardgame
from model.review import Review
from schemas.api_schema import *

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

    @staticmethod
    def boardgame_and_reviews_to_detail_response(boardgame_display_response: BoardgameDisplayResponse, reviews: list[
        ReviewDisplayResponse]) -> BoardgameDetailResponse:
        return BoardgameDetailResponse(
            id=boardgame_display_response.id,
            name=boardgame_display_response.name,
            producer=boardgame_display_response.producer,
            description=boardgame_display_response.description,
            price=boardgame_display_response.price,
            numberOfCopies=boardgame_display_response.numberOfCopies,
            minNumberOfPlayers=boardgame_display_response.minNumberOfPlayers,
            maxNumberOfPlayers=boardgame_display_response.maxNumberOfPlayers,
            thumbnailURL=boardgame_display_response.thumbnailURL,
            tags=boardgame_display_response.tags,
            reviews=reviews
        )