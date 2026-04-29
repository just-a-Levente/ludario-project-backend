from schemas.boardgame_api_mapper import *
from repository.boardgame_repository import BoardgameRepository
from services.validator_service import BoardgameValidator

class BoardgameService:

    def __init__(self, repository: BoardgameRepository):
        self.__repository = repository

    def get_all_boardgames(self) -> list[BoardgameDisplayResponse]:
        boardgames = self.__repository.get_all_boardgames
        return [BoardgameAPIMapper.boardgame_to_display_response(boardgame) for boardgame in boardgames]

    def get_boardgames(self, offset: int, limit: int) -> PaginatedBoardgamesResponse:
        boardgames = self.__repository.get_boardgames(offset, limit)
        total_count = self.__repository.get_number_of_boardgames

        return PaginatedBoardgamesResponse(
            items=[BoardgameAPIMapper.boardgame_to_display_response(boardgame) for boardgame in boardgames],
            total_count=total_count,
            offset=offset,
            limit=limit
        )

    def get_boardgame(self, boardgame_id: int) -> BoardgameDisplayResponse:
        boardgame = self.__repository.get_boardgame(boardgame_id)
        return BoardgameAPIMapper.boardgame_to_display_response(boardgame)

    def create_boardgame(self, create_request: BoardgameCreateRequest) -> BoardgameDisplayResponse:
        BoardgameValidator().validate_boardgame_input(create_request)
        boardgame_instance = BoardgameAPIMapper.create_boardgame_from_request(create_request)
        self.__repository.insert_boardgame(boardgame_instance)
        return BoardgameAPIMapper.boardgame_to_display_response(boardgame_instance)

    def delete_boardgame(self, boardgame_id: int):
        self.__repository.delete_boardgame(boardgame_id)

    def update_boardgame(self, update_request: BoardgameUpdateRequest) -> BoardgameDisplayResponse:
        BoardgameValidator().validate_boardgame_input(update_request)
        updated_boardgame_instance = BoardgameAPIMapper.update_boardgame_from_request(update_request)
        self.__repository.update_boardgame(updated_boardgame_instance)
        return BoardgameAPIMapper.boardgame_to_display_response(updated_boardgame_instance)

repo = BoardgameRepository()
boardgame_service = BoardgameService(repo)