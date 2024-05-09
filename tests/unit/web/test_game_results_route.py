from fastapi.testclient import TestClient

from tests.page_objects.game_results_page import GameResultsPage
from voting24.game.game import Game


def game_results_page_should_return_404_if_game_is_not_found(testclient: TestClient, finished_game: Game) -> None:
    page = GameResultsPage.open(testclient, "some-key")
    assert page.response.status_code == 404


def game_results_page_should_contain_game_name_in_title(testclient: TestClient, finished_game: Game) -> None:
    page = GameResultsPage.open(testclient, finished_game.key)
    assert page.response.status_code == 200
    assert finished_game.name in page.title()


def game_results_page_should_contain_all_game_items(testclient: TestClient, finished_game: Game) -> None:
    page = GameResultsPage.open(testclient, finished_game.key)
    assert page.response.status_code == 200
    results = page.results()
    assert len(results) == len(finished_game.items)
