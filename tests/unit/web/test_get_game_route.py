from fastapi.testclient import TestClient

from tests.page_objects.game_page import GamePage
from voting24.game.game import Game


def main_game_page_should_contain_game_name(testclient: TestClient, game: Game) -> None:
    page = GamePage.open(testclient, game.key)
    assert page.name() == game.name


def main_game_page_should_contain_game_name_in_the_title(testclient: TestClient, game: Game) -> None:
    page = GamePage.open(testclient, game.key)
    assert game.name in page.title()


def main_game_page_should_contain_join_form(testclient: TestClient, game: Game) -> None:
    page = GamePage.open(testclient, game.key)
    form = page.join_form_fields()
    assert form["game_key"].attrs["value"] == game.key
    assert form["player_name"]


def main_game_page_should_contain_join_form_with_correct_target(testclient: TestClient, game: Game) -> None:
    page = GamePage.open(testclient, game.key)
    form = page.join_form()
    assert form.attrs["action"] == f"/game/{game.key}/join"
    assert form.attrs["method"] == "POST"


def main_game_page_should_respond_with_422_if_game_key_is_invalid(testclient: TestClient) -> None:
    response = testclient.get("/game/some.invalid.key")
    assert response.status_code == 422


def main_game_page_should_respond_with_422_if_game_key_is_too_long(testclient: TestClient) -> None:
    response = testclient.get("/game/" + "a" * 100)
    assert response.status_code == 422


def main_game_css_should_respond_with_404_if_game_has_no_style(testclient: TestClient, game: Game) -> None:
    response = testclient.get(f"/game/{game.key}/custom.css")
    assert response.status_code == 404


def main_game_css_should_respond_with_200_if_game_has_style(testclient: TestClient, game: Game) -> None:
    game.css = "body { color: red; }"
    response = testclient.get(f"/game/{game.key}/custom.css")
    assert response.status_code == 200
    assert response.text == "body { color: red; }"
