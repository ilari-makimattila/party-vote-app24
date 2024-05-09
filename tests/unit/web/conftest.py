import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from voting24.db.database import Database, InMemoryDatabase
from voting24.game.game import Choice, Game, VoteItem
from voting24.web.dependencies import get_database


@pytest.fixture()
def database() -> Database:
    return InMemoryDatabase()


@pytest.fixture()
def app(database: Database) -> FastAPI:
    from voting24.web.app import app
    app.dependency_overrides[get_database] = lambda: database
    return app


@pytest.fixture()
def testclient(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture()
def game(database: Database) -> Game:
    g = Game.new(name="default game name")
    g.items = [
        VoteItem(key="key1", title="Vote item 1", text="Vote item 1 description", options=[
            Choice(key="choicekey1", text="Choice A", value=1),
            Choice(key="choicekey2", text="Choice B", value=2),
        ]),
        VoteItem(key="key2", title="Vote item 2", text="Vote item 2 description", options=[
            Choice(key="choicekey1", text="Choice A", value=1),
            Choice(key="choicekey2", text="Choice B", value=2),
        ]),
    ]
    database.save_game(g)
    return g


@pytest.fixture()
def finished_game(database: Database) -> Game:
    g = Game.new(name="finished game name")
    g.items = [
        VoteItem(key="key1", icon="👍", title="Vote item 1", text="Vote item 1 description", options=[
            Choice(key="choicekey1", text="Choice A", value=-1),
            Choice(key="choicekey2", text="Choice B", value=0),
            Choice(key="choicekey3", text="Choice C", value=1),
        ]),
        VoteItem(key="key2", title="Vote item 2", text="Vote item 2 description", options=[
            Choice(key="choicekey1", text="Choice A", value=-1),
            Choice(key="choicekey2", text="Choice B", value=0),
            Choice(key="choicekey3", text="Choice C", value=1),
        ]),
    ]
    database.save_game(g)
    player_1 = database.join_game(g.key, "player 1")
    player_2 = database.join_game(g.key, "player 2")
    player_3 = database.join_game(g.key, "player 3")
    database.vote(player_1.name, g.key, g.items[0].key, g.items[0].options[0].key)
    database.vote(player_2.name, g.key, g.items[0].key, g.items[0].options[0].key)
    database.vote(player_3.name, g.key, g.items[0].key, g.items[0].options[1].key)
    database.vote(player_1.name, g.key, g.items[1].key, g.items[1].options[1].key)
    database.vote(player_2.name, g.key, g.items[1].key, g.items[1].options[2].key)
    database.vote(player_3.name, g.key, g.items[1].key, g.items[1].options[2].key)

    return g
