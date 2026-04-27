from schemas.api_schema import BoardgameCreateRequest, BoardgameUpdateRequest
import json

class BoardgameValidationException(Exception):
    def __init__(self, errors: dict[str, str]):
        super().__init__(json.dumps(errors))

class BoardgameValidator:

    def __init__(self):
        self.__errors: dict[str, str] = {}

    def __validate_not_empty_string(self, field: str, text: str) -> None:
        if len(text) == 0:
            self.__errors[field] = f"{field} can't be empty"

    def __validate_positive_integer(self, field: str, integer_input: str):
        if not integer_input.isdigit():
            self.__errors[field] = f"{field} can't be parsed as an integer"

        parsed_integer = int(integer_input)
        if parsed_integer <= 0:
            self.__errors[field] = f"{field} must be non-zero"

    def __validate_positive_float(self, field: str, float_input: str):
        try:
            parsed_float = float(float_input)
            if parsed_float <= 0:
                self.__errors[field] = f"{field} must be positive and non-zero"
        except:
            self.__errors[field] = f"{field} can't be parsed as a float"

    def __validate_player_count(self, min_player_count: int, max_player_count: int):
        if min_player_count > max_player_count:
            self.__errors["player_count"] = "Minimum player count must be less than or equal to maximum player count"


    def validate_boardgame_input(self, request: BoardgameCreateRequest | BoardgameUpdateRequest):
        self.__validate_not_empty_string("name", request.name)
        self.__validate_not_empty_string("producer", request.producer)
        self.__validate_not_empty_string("description", request.description)
        self.__validate_positive_float("price", request.price)
        self.__validate_positive_integer("numberOfCopies", request.numberOfCopies)
        self.__validate_positive_integer("minNumberOfPlayers", request.minNumberOfPlayers)
        self.__validate_positive_integer("maxNumberOfPlayers", request.maxNumberOfPlayers)
        self.__validate_not_empty_string("thumbnailURL", request.thumbnailURL)
        self.__validate_not_empty_string("tags", request.tags)

        if len(self.__errors) > 0:
            exception_errors = self.__errors.copy()
            self.__errors = {}
            raise BoardgameValidationException(exception_errors)

        self.__errors = {}