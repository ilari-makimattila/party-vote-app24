from fastapi.testclient import TestClient

from voting24.db.database import Database
from voting24.game.game import Game


def play_item_should_return_404_if_game_does_not_exist(testclient: TestClient, game: Game) -> None:
    response = testclient.get(
        "/game/unknowngame/item",
        follow_redirects=False,
        cookies={"player_name": "My Name"},
    )
    assert response.status_code == 404


def play_item_should_return_303_to_game_if_player_is_not_set(testclient: TestClient, game: Game) -> None:
    response = testclient.get(
        f"/game/{game.key}/item",
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert response.headers["Location"] == f"/game/{game.key}"


def play_item_should_return_303_to_game_if_player_does_not_exist(testclient: TestClient, game: Game) -> None:
    response = testclient.get(
        f"/game/{game.key}/item",
        follow_redirects=False,
        cookies={"player_name": "My Name"},
    )
    assert response.status_code == 303
    assert response.headers["Location"] == f"/game/{game.key}"


def play_item_should_return_303_to_first_item(testclient: TestClient, database: Database, game: Game) -> None:
    database.join_game(game.key, "My Name")
    response = testclient.get(
        f"/game/{game.key}/item",
        follow_redirects=False,
        cookies={"player_name": "My Name"},
    )
    assert response.status_code == 303
    assert response.headers["Location"] == f"/game/{game.key}/item/key1"


def play_item_should_return_303_to_first_unvoted_item(testclient: TestClient, database: Database, game: Game) -> None:
    database.join_game(game.key, "My Name")
    database.vote("My Name", game.key, game.items[0].key, game.items[0].options[0].key)
    response = testclient.get(
        f"/game/{game.key}/item",
        follow_redirects=False,
        cookies={"player_name": "My Name"},
    )
    assert response.status_code == 303
    assert response.headers["Location"] == f"/game/{game.key}/item/key2"


def play_item_page_should_return_404_if_game_does_not_exist(testclient: TestClient, game: Game) -> None:
    response = testclient.get(
        "/game/unknowngame/item/foo",
        follow_redirects=False,
        cookies={"player_name": "My Name"},
    )
    assert response.status_code == 404


def play_item_page_should_return_303_to_game_if_player_is_not_set(testclient: TestClient, game: Game) -> None:
    response = testclient.get(
        f"/game/{game.key}/item/key1",
        follow_redirects=False,
    )
    assert response.status_code == 303
    assert response.headers["Location"] == f"/game/{game.key}"


def play_item_page_should_return_303_to_game_if_player_does_not_exist(testclient: TestClient, game: Game) -> None:
    response = testclient.get(
        f"/game/{game.key}/item/key1",
        follow_redirects=False,
        cookies={"player_name": "My Name"},
    )
    assert response.status_code == 303
    assert response.headers["Location"] == f"/game/{game.key}"


def play_item_page_should_return_404_if_item_does_not_exist(
    testclient: TestClient,
    database: Database,
    game: Game,
) -> None:
    database.join_game(game.key, "My Name")
    response = testclient.get(
        f"/game/{game.key}/item/foo",
        follow_redirects=False,
        cookies={"player_name": "My Name"},
    )
    assert response.status_code == 404
