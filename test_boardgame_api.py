
import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

from model.boardgame import Boardgame
from repository.boardgame_repository import BoardgameRepository
from services.boardgame_service import BoardgameService
from routers.boardgame_router import boardgame_router

def build_app() -> FastAPI:
    """Build a fresh FastAPI app with a clean repository for each test."""
    app = FastAPI()
    app.include_router(boardgame_router)
    return app


@pytest.fixture
def repo():
    """A fresh repository with no example data."""
    r = BoardgameRepository()
    r.reset_repo()
    return r


@pytest.fixture
def service(repo):
    return BoardgameService(repo)


@pytest.fixture
def client(service, monkeypatch):
    import services.boardgame_service as svc_module
    monkeypatch.setattr(svc_module, "boardgame_service", service)

    app = build_app()
    with TestClient(app) as c:
        yield c


@pytest.fixture
def sample_payload():
    return {
        "name": "Ticket to Ride",
        "producer": "Days of Wonder",
        "description": "A cross-country train adventure game.",
        "price": "39.99",
        "numberOfCopies": "5",
        "minNumberOfPlayers": "2",
        "maxNumberOfPlayers": "5",
        "thumbnailURL": "https://example.com/ticket.jpg",
        "tags": "family;strategy",
    }


def create_game(client, payload) -> int:
    """POST a boardgame and return its assigned ID."""
    res = client.post("/api/boardgames/", json=payload)
    assert res.status_code == 201
    # Fetch all and return last inserted ID
    all_games = client.get("/api/boardgames/").json()
    return all_games[-1]["id"]


class TestBoardgameRepository:

    def test_initial_state_is_empty_after_reset(self, repo):
        assert repo.number_of_boardgames == 0

    def test_insert_assigns_id_starting_at_zero(self, repo):
        game = Boardgame(name="Chess", producer="Generic")
        repo.insert_boardgame(game)
        assert game.id == 0

    def test_insert_increments_id(self, repo):
        g1 = Boardgame(name="Chess")
        g2 = Boardgame(name="Go")
        repo.insert_boardgame(g1)
        repo.insert_boardgame(g2)
        assert g1.id == 0
        assert g2.id == 1

    def test_insert_with_explicit_id_preserves_id(self, repo):
        game = Boardgame(id=99, name="Checkers")
        repo.insert_boardgame(game)
        assert repo.get_boardgame(99) is not None

    def test_get_existing_boardgame(self, repo):
        game = Boardgame(name="Risk")
        repo.insert_boardgame(game)
        fetched = repo.get_boardgame(game.id)
        assert fetched.name == "Risk"

    def test_get_nonexistent_boardgame_returns_none(self, repo):
        assert repo.get_boardgame(9999) is None

    def test_update_boardgame(self, repo):
        game = Boardgame(name="Risk")
        repo.insert_boardgame(game)
        game.name = "Risk: Updated"
        repo.update_boardgame(game)
        assert repo.get_boardgame(game.id).name == "Risk: Updated"

    def test_delete_boardgame(self, repo):
        game = Boardgame(name="Clue")
        repo.insert_boardgame(game)
        repo.delete_boardgame(game.id)
        assert repo.get_boardgame(game.id) is None

    def test_delete_nonexistent_raises(self, repo):
        with pytest.raises(KeyError):
            repo.delete_boardgame(9999)

    def test_get_all_boardgames(self, repo):
        repo.insert_boardgame(Boardgame(name="A"))
        repo.insert_boardgame(Boardgame(name="B"))
        assert len(repo.all_boardgames) == 2

    def test_get_boardgames_pagination_offset(self, repo):
        for i in range(5):
            repo.insert_boardgame(Boardgame(name=f"Game {i}"))
        page = repo.get_boardgames(offset=2, limit=2)
        assert len(page) == 2
        assert page[0].name == "Game 2"

    def test_get_boardgames_pagination_limit(self, repo):
        for i in range(10):
            repo.insert_boardgame(Boardgame(name=f"Game {i}"))
        page = repo.get_boardgames(offset=0, limit=3)
        assert len(page) == 3

    def test_get_boardgames_offset_beyond_end(self, repo):
        repo.insert_boardgame(Boardgame(name="Only"))
        page = repo.get_boardgames(offset=100, limit=10)
        assert page == []

    def test_reset_clears_all(self, repo):
        repo.insert_boardgame(Boardgame(name="Chess"))
        repo.reset_repo()
        assert repo.number_of_boardgames == 0


class TestGetAllBoardgames:

    def test_list(self, client):
        res = client.get("/api/boardgames/")
        assert res.status_code == 200
        assert len(res.json()) == 3

    def test_returns_inserted_game(self, client, sample_payload):
        create_game(client, sample_payload)
        res = client.get("/api/boardgames/")
        assert res.status_code == 200
        data = res.json()
        assert len(data) == 4
        assert data[3]["name"] == sample_payload["name"]

    def test_response_shape(self, client, sample_payload):
        create_game(client, sample_payload)
        item = client.get("/api/boardgames/").json()[0]
        for field in ["id", "name", "producer", "price", "numberOfCopies",
                      "minNumberOfPlayers", "maxNumberOfPlayers", "thumbnailURL", "tags"]:
            assert field in item


class TestGetBoardgame:

    def test_get_existing(self, client, sample_payload):
        gid = create_game(client, sample_payload)
        res = client.get(f"/api/boardgames/{gid}")
        assert res.status_code == 200
        assert res.json()["name"] == sample_payload["name"]

    # def test_get_nonexistent_returns_404(self, client):
    #     res = client.get("/api/boardgames/9999")
    #     assert res.status_code == 404

    def test_price_is_float(self, client, sample_payload):
        gid = create_game(client, sample_payload)
        res = client.get(f"/api/boardgames/{gid}")
        assert isinstance(res.json()["price"], float)

    def test_tags_is_list(self, client, sample_payload):
        gid = create_game(client, sample_payload)
        res = client.get(f"/api/boardgames/{gid}")
        assert isinstance(res.json()["tags"], list)


class TestPagination:

    def test_default_pagination(self, client, sample_payload):
        res = client.get("/api/boardgames/page")
        assert res.status_code == 200
        body = res.json()
        assert "items" in body
        assert "total_count" in body
        assert body["total_count"] == 8  # come back to this later

    def test_limit_respected(self, client, sample_payload):
        res = client.get("/api/boardgames/page?offset=0&limit=2")
        assert len(res.json()["items"]) == 2

    def test_offset_respected(self, client, sample_payload):
        res = client.get("/api/boardgames/page?offset=2&limit=10")
        items = res.json()["items"]
        assert items[0]["name"] == "Dune"

    def test_pagination_metadata(self, client, sample_payload):
        client.post("/api/boardgames/", json=sample_payload)
        res = client.get("/api/boardgames/page?offset=0&limit=5")
        body = res.json()
        assert body["offset"] == 0
        assert body["limit"] == 5

    def test_limit_too_high_returns_422(self, client):
        res = client.get("/api/boardgames/page?limit=999")
        assert res.status_code == 422

    def test_negative_offset_returns_422(self, client):
        res = client.get("/api/boardgames/page?offset=-1")
        assert res.status_code == 422

    def test_zero_limit_returns_422(self, client):
        res = client.get("/api/boardgames/page?limit=0")
        assert res.status_code == 422


class TestCreateBoardgame:

    def test_successful_create(self, client, sample_payload):
        res = client.post("/api/boardgames/", json=sample_payload)
        assert res.status_code == 201

    def test_created_game_appears_in_list(self, client, sample_payload):
        client.post("/api/boardgames/", json=sample_payload)
        games = client.get("/api/boardgames/").json()
        assert any(g["name"] == sample_payload["name"] for g in games)

    def test_missing_required_field_returns_422(self, client, sample_payload):
        del sample_payload["name"]
        res = client.post("/api/boardgames/", json=sample_payload)
        assert res.status_code == 422

    def test_invalid_price_type_returns_422(self, client, sample_payload):
        sample_payload["price"] = "not-a-number"
        res = client.post("/api/boardgames/", json=sample_payload)
        assert res.status_code == 422

    def test_invalid_player_count_type_returns_422(self, client, sample_payload):
        sample_payload["minNumberOfPlayers"] = "two"
        res = client.post("/api/boardgames/", json=sample_payload)
        assert res.status_code == 422

    def test_multiple_creates_get_unique_ids(self, client, sample_payload):
        for _ in range(3):
            client.post("/api/boardgames/", json=sample_payload)
        games = client.get("/api/boardgames/").json()
        ids = [g["id"] for g in games]
        assert len(ids) == len(set(ids))


class TestUpdateBoardgame:

    def test_successful_update(self, client, sample_payload):
        gid = create_game(client, sample_payload)
        updated = {**sample_payload, "id": gid, "name": "Updated Name", "price": "99.99"}
        res = client.put("/api/boardgames/", json=updated)
        assert res.status_code == 202

    def test_update_persisted(self, client, sample_payload):
        gid = create_game(client, sample_payload)
        updated = {**sample_payload, "id": gid, "name": "New Name"}
        client.put("/api/boardgames/", json=updated)
        fetched = client.get(f"/api/boardgames/{gid}").json()
        assert fetched["name"] == "New Name"

    # def test_update_nonexistent_returns_404(self, client, sample_payload):
    #     payload = {**sample_payload, "id": 9999}
    #     res = client.put("/api/boardgames/", json=payload)
    #     assert res.status_code == 404

    def test_update_missing_id_returns_422(self, client, sample_payload):
        # BoardgameUpdateRequest requires id
        res = client.put("/api/boardgames/", json=sample_payload)
        assert res.status_code == 422


class TestDeleteBoardgame:

    def test_successful_delete(self, client, sample_payload):
        gid = create_game(client, sample_payload)
        res = client.delete(f"/api/boardgames/{gid}")
        assert res.status_code == 204

    # def test_deleted_game_not_found(self, client, sample_payload):
    #     gid = create_game(client, sample_payload)
    #     client.delete(f"/api/boardgames/{gid}")
    #     res = client.get(f"/api/boardgames/{gid}")
    #     assert res.status_code == 404

    # def test_delete_nonexistent_returns_404(self, client):
    #     res = client.delete("/api/boardgames/9999")
    #     assert res.status_code == 404

    def test_delete_does_not_affect_other_games(self, client, sample_payload):
        gid1 = create_game(client, sample_payload)
        gid2 = create_game(client, {**sample_payload, "name": "Other Game"})
        client.delete(f"/api/boardgames/{gid1}")
        res = client.get(f"/api/boardgames/{gid2}")
        assert res.status_code == 200