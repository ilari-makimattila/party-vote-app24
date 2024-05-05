from fastapi.testclient import TestClient

from tests.page_objects.game_page import GamePage
from voting24.game.game import Game


def main_game_page_should_contain_game_name(testclient: TestClient, game: Game) -> None:
    page = GamePage.open(testclient, game.key)
    assert page.name() == game.name
