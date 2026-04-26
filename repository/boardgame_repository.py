from model.boardgame import Boardgame

class BoardgameRepository:
    def __init__(self):
        self.boardgames: dict[int, Boardgame] = {}
        self.lastID: int = 0

    def reset_repo(self):
        self.boardgames = {}
        self.lastID = 0

    @property
    def number_of_boardgames(self) -> int:
        return len(self.boardgames)

    @property
    def get_last_id(self) -> int:
        return self.lastID

    def increment_last_id(self):
        self.lastID += 1

    def get_boardgame(self, boardgame_id: int) -> Boardgame | None:
        return self.boardgames.get(boardgame_id)

    def insert_boardgame(self, new_boardgame: Boardgame):
        if new_boardgame.id == -1:
            new_id = self.get_last_id
            self.increment_last_id()
            new_boardgame.id = new_id
        self.boardgames[new_boardgame.id] = new_boardgame

    def update_boardgame(self, updated_boardgame: Boardgame):
        self.boardgames[updated_boardgame.id] = updated_boardgame

    def delete_boardgame(self, boardgame_id_to_delete: int):
        self.boardgames.pop(boardgame_id_to_delete)