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
    form = page.join_form()
    assert form["game_key"].attrs["value"] == game.key
    assert form["player_name"]
