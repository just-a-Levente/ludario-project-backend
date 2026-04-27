from model.boardgame import Boardgame

class BoardgameRepository:

    def __init__(self):
        self.boardgames: dict[int, Boardgame] = {}
        self.lastID: int = 0
        self.__fill_with_examples()

    def __fill_with_examples(self):
        self.insert_boardgame(Boardgame(
            id=-1,
            name="Saboteur",
            producer="Piatnik",
            description="Description of Saboteur",
            price=8.99,
            numberOfCopies=12,
            minNumberOfPlayers=4,
            maxNumberOfPlayers=6,
            thumbnailURL="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fkuplayboardgamestore.com%2Fwp-content%2Fuploads%2F2023%2F08%2Fsaboteur-box.jpg&f=1&nofb=1&ipt=81572d0cfaa7bb2617cd861785c23c9dc3aa9058f5a3ac37eb3a9ef53e7f0a6c",
            tags=["social deduction", "mining"]
        ))
        self.insert_boardgame(Boardgame(
            id=-1,
            name="Settlers of Catan",
            producer="Kosmos",
            description="Description of Settlers of Catan",
            price=14.99,
            numberOfCopies=12,
            minNumberOfPlayers=4,
            maxNumberOfPlayers=6,
            thumbnailURL="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.catan.com%2Fsites%2Fdefault%2Ffiles%2F2021-07%2F0001021_catan-25th-anniversary-edition.png&f=1&nofb=1&ipt=0690943ce60e9167480837ac28fcd490b57c76a310bdc433203130f5a2a6dcc1",
            tags=["social deduction", "colony builder"]
        ))
        self.insert_boardgame(Boardgame(
            id=-1,
            name="Dune",
            producer="Gale Force Nine",
            description="Description of Dune",
            price=21.99,
            numberOfCopies=4,
            minNumberOfPlayers=3,
            maxNumberOfPlayers=6,
            thumbnailURL="https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fwww.belloflostsouls.net%2Fwp-content%2Fuploads%2F2019%2F06%2FDune-Box-Left-Small.jpg&f=1&nofb=1&ipt=6d876cfe897e070c657cc0d94248be93e4a8c0e4e4da99628d4e1bf387b68d6f",
            tags=["social deduction", "colony builder"]
        ))

    def reset_repo(self):
        self.boardgames = {}
        self.lastID = 0

    @property
    def get_boardgames(self) -> list[Boardgame]:
        return list(self.boardgames.values())

    @property
    def number_of_boardgames(self) -> int:
        return len(self.boardgames)

    @property
    def get_last_id(self) -> int:
        return self.lastID

    def __increment_last_id(self):
        self.lastID += 1

    def get_boardgame(self, boardgame_id: int) -> Boardgame | None:
        return self.boardgames.get(boardgame_id)

    def insert_boardgame(self, new_boardgame: Boardgame):
        if new_boardgame.id == -1:
            new_id = self.get_last_id
            self.__increment_last_id()
            new_boardgame.id = new_id
        self.boardgames[new_boardgame.id] = new_boardgame

    def update_boardgame(self, updated_boardgame: Boardgame):
        self.boardgames[updated_boardgame.id] = updated_boardgame

    def delete_boardgame(self, boardgame_id_to_delete: int):
        self.boardgames.pop(boardgame_id_to_delete)