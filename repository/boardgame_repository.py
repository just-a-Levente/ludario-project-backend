from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from model.boardgame import Boardgame
from model.tables import Base, BoardgameORM
from db import SessionLocal

class BoardgameRepository:

    def __init__(self):
        self.__fill_with_examples()

    def __fill_with_examples(self):
        if self.number_of_boardgames > 0:
            return  # don't re-seed if data already exists
        self.insert_boardgame(Boardgame(
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

    @property
    def all_boardgames(self) -> list[Boardgame]:
        with SessionLocal() as session:
            orms = session.query(BoardgameORM).all()
            return [self.__to_model(orm) for orm in orms]

    @property
    def number_of_boardgames(self) -> int:
        with SessionLocal() as session:
            return session.query(func.count(BoardgameORM.id)).scalar()

    def __to_model(self, orm: BoardgameORM) -> Boardgame:
        return Boardgame(
            id=orm.id,
            hidden=orm.hidden,
            name=orm.name,
            producer=orm.producer,
            description=orm.description,
            price=orm.price,
            numberOfCopies=orm.numberOfCopies,
            minNumberOfPlayers=orm.minNumberOfPlayers,
            maxNumberOfPlayers=orm.maxNumberOfPlayers,
            thumbnailURL=orm.thumbnailURL,
            tags=orm.tags.split(";") if orm.tags else [],
        )

    def get_boardgame(self, boardgame_id: int) -> Boardgame | None:
        with SessionLocal() as session:
            orm = session.get(BoardgameORM, boardgame_id)
            return self.__to_model(orm) if orm else None

    def get_boardgames(self, offset: int, limit: int) -> list[Boardgame]:
        with SessionLocal() as session:
            orms = session.query(BoardgameORM).offset(offset).limit(limit).all()
            return [self.__to_model(orm) for orm in orms]

    def insert_boardgame(self, new_boardgame: Boardgame):
        with SessionLocal() as session:
            orm = BoardgameORM(
                name=new_boardgame.name,
                hidden=new_boardgame.hidden,
                producer=new_boardgame.producer,
                description=new_boardgame.description,
                price=new_boardgame.price,
                numberOfCopies=new_boardgame.numberOfCopies,
                minNumberOfPlayers=new_boardgame.minNumberOfPlayers,
                maxNumberOfPlayers=new_boardgame.maxNumberOfPlayers,
                thumbnailURL=new_boardgame.thumbnailURL,
                tags=";".join(new_boardgame.tags),
            )
            session.add(orm)
            session.commit()
            session.refresh(orm)
            new_boardgame.id = orm.id
            return new_boardgame

    def update_boardgame(self, updated_boardgame: Boardgame):
        with SessionLocal() as session:
            orm = session.get(BoardgameORM, updated_boardgame.id)
            if orm is None:
                return
            orm.hidden = updated_boardgame.hidden
            orm.name = updated_boardgame.name
            orm.producer = updated_boardgame.producer
            orm.description = updated_boardgame.description
            orm.price = updated_boardgame.price
            orm.numberOfCopies = updated_boardgame.numberOfCopies
            orm.minNumberOfPlayers = updated_boardgame.minNumberOfPlayers
            orm.maxNumberOfPlayers = updated_boardgame.maxNumberOfPlayers
            orm.thumbnailURL = updated_boardgame.thumbnailURL
            orm.tags = ";".join(updated_boardgame.tags)
            session.commit()

    def delete_boardgame(self, boardgame_id_to_delete: int):
        with SessionLocal() as session:
            orm = session.get(BoardgameORM, boardgame_id_to_delete)
            if orm:
                session.delete(orm)
                session.commit()