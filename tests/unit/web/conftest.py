from collections.abc import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from voting24.db.database import Database, InMemoryDatabase
from voting24.game.game import Choice, Game, VoteItem
from voting24.web.dependencies import get_database


@pytest.fixture()
def app() -> FastAPI:
    from voting24.web.app import app
    return app


@pytest.fixture()
def testclient(app: FastAPI) -> TestClient:
    return TestClient(app)


@pytest.fixture()
def database(app: FastAPI) -> Generator[Database, None, None]:
    db = InMemoryDatabase()
    app.dependency_overrides[get_database] = lambda: db
    yield db
    del app.dependency_overrides[get_database]


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
