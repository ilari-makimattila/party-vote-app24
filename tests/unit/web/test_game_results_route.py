from fastapi.testclient import TestClient

from tests.page_objects.game_results_page import GameResultsPage
from voting24.game.game import Game


def game_results_page_should_return_404_if_game_is_not_found(testclient: TestClient) -> None:
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


def game_results_page_should_have_correct_results(testclient: TestClient, finished_game: Game) -> None:
    page = GameResultsPage.open(testclient, finished_game.key)
    assert page.response.status_code == 200
    results = page.results()
    assert results[0] == (finished_game.items[1].title, 2)
    assert results[1] == (finished_game.items[0].title, -2)


def game_results_page_should_have_a_link_to_the_first_item(testclient: TestClient, finished_game: Game) -> None:
    page = GameResultsPage.open(testclient, finished_game.key)
    assert page.response.status_code == 200
    first_item_link = page.first_item_link()
    assert first_item_link.attrs["href"] == f"/game/{finished_game.key}/item/{finished_game.items[0].key}"


def game_results_page_should_have_links_to_all_items(testclient: TestClient, finished_game: Game) -> None:
    page = GameResultsPage.open(testclient, finished_game.key)
    assert page.response.status_code == 200
    item_links = page.all_item_links()
    assert len(item_links) == len(finished_game.items)
    assert item_links[0].attrs["href"] == f"/game/{finished_game.key}/item/{finished_game.items[1].key}"
    assert item_links[1].attrs["href"] == f"/game/{finished_game.key}/item/{finished_game.items[0].key}"
