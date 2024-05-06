from fastapi.testclient import TestClient

from tests.page_objects.game_page import GamePage
from voting24.db.database import Database
from voting24.game.game import Game


def join_game_post_should_return_404_if_game_does_not_exist(testclient: TestClient, game: Game) -> None:
    response = testclient.post(
        "/game/unknowngame/join",
        data={"player_name": "My Name"},
        follow_redirects=False,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 404


def join_game_post_should_return_400_and_show_the_form_with_force_if_player_already_exists(
    testclient: TestClient,
    database: Database,
    game: Game,
) -> None:
    database.join_game(game.key, "A player")
    response = testclient.post(
        f"/game/{game.key}/join",
        data={"player_name": "A player"},
        follow_redirects=False,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 400
    page = GamePage(response)
    form = page.join_form()
    assert form["player_name"].attrs["value"] == "A player"
    assert form["force"].attrs["checked"] is not None
    assert form["force"].attrs["value"] == "1"


def join_game_post_should_set_cookie_and_redirect(testclient: TestClient, game: Game) -> None:
    response = testclient.post(
        f"/game/{game.key}/join",
        data={"player_name": "My Name"},
        follow_redirects=False,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    print(response.text)
    assert response.status_code == 303
    assert response.cookies["player_name"] == '"My Name"'
    assert response.headers["Location"] == f"/game/{game.key}/item"


def join_game_post_should_set_cookie_and_redirect_when_player_exists_and_join_as_existing(
    testclient: TestClient,
    database: Database,
    game: Game,
) -> None:
    database.join_game(game.key, "The player")
    response = testclient.post(
        f"/game/{game.key}/join",
        data={"player_name": "The player", "force": "1"},
        follow_redirects=False,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    print(response.text)
    assert response.status_code == 303
    assert response.cookies["player_name"] == '"The player"'
    assert response.headers["Location"] == f"/game/{game.key}/item"
