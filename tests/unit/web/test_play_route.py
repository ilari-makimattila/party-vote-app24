from fastapi.testclient import TestClient

from tests.page_objects.game_item_page import GameItemPage
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


def play_item_page_should_show_vote_item_in_title(testclient: TestClient, database: Database, game: Game) -> None:
    database.join_game(game.key, "My Name")
    response = testclient.get(
        f"/game/{game.key}/item/key1",
        follow_redirects=False,
        cookies={"player_name": "My Name"},
    )
    assert response.status_code == 200
    page = GameItemPage(response)
    assert "Vote item 1" in page.title()


def play_item_page_should_show_vote_form(testclient: TestClient, database: Database, game: Game) -> None:
    database.join_game(game.key, "My Name")
    response = testclient.get(
        f"/game/{game.key}/item/{game.items[0].key}",
        follow_redirects=False,
        cookies={"player_name": "My Name"},
    )
    assert response.status_code == 200
    page = GameItemPage(response)
    vote_form = page.vote_form()
    game_key_input = vote_form.select_one("input[name=game_key]")
    item_key_input = vote_form.select_one("input[name=item_key]")
    assert game_key_input
    assert item_key_input
    assert game_key_input.attrs["value"] == game.key
    assert item_key_input.attrs["value"] == game.items[0].key
    votes = vote_form.select("input[name=vote]")
    for (vote_tag, choice) in zip(votes, game.items[0].options, strict=True):
        assert vote_tag.attrs["value"] == choice.key


def play_item_page_vote_form_should_have_correct_route(testclient: TestClient, database: Database, game: Game) -> None:
    database.join_game(game.key, "My Name")
    response = testclient.get(
        f"/game/{game.key}/item/{game.items[1].key}",
        follow_redirects=False,
        cookies={"player_name": "My Name"},
    )
    assert response.status_code == 200
    page = GameItemPage(response)
    vote_form = page.vote_form()
    assert vote_form.attrs["action"] == f"/game/{game.key}/item/{game.items[1].key}"
    assert vote_form.attrs["method"] == "POST"


def post_play_item_vote_should_return_404_if_game_is_not_found(testclient: TestClient, game: Game) -> None:
    response = testclient.post(
        f"/game/somenonexistinggame/item/{game.items[1].key}",
        follow_redirects=False,
        cookies={"player_name": "My Name"},
        data={"game_key": game.key, "item_key": game.items[1].key, "vote": game.items[1].options[0].key},
    )
    assert response.status_code == 404


def post_play_item_vote_should_return_404_if_item_is_not_found(
    testclient: TestClient,
    database: Database,
    game: Game,
) -> None:
    database.join_game(game.key, "My Name")
    response = testclient.post(
        f"/game/{game.key}/item/somenonexistingitem",
        follow_redirects=False,
        cookies={"player_name": "My Name"},
        data={"game_key": game.key, "item_key": game.items[1].key, "vote": game.items[1].options[0].key},
    )
    assert response.status_code == 404


def post_play_item_vote_should_return_303_to_game_if_player_does_not_exist(testclient: TestClient, game: Game) -> None:
    response = testclient.post(
        f"/game/{game.key}/item/{game.items[1].key}",
        follow_redirects=False,
        cookies={"player_name": "My Name"},
        data={"game_key": game.key, "item_key": game.items[1].key, "vote": game.items[1].options[0].key},
    )
    assert response.status_code == 303
    assert response.headers["Location"] == f"/game/{game.key}"


def post_play_item_vote_should_save_the_vote(testclient: TestClient, database: Database, game: Game) -> None:
    database.join_game(game.key, "My Name")
    testclient.post(
        f"/game/{game.key}/item/{game.items[1].key}",
        follow_redirects=False,
        cookies={"player_name": "My Name"},
        data={"game_key": game.key, "item_key": game.items[1].key, "vote": game.items[1].options[0].key},
    )
    player = database.load_game(game.key).player("My Name")
    assert player
    assert player.votes == {game.items[1].key: game.items[1].options[0].key}


def post_play_item_vote_should_return_303_to_next_unvoted_game_item_page(
    testclient: TestClient,
    database: Database,
    game: Game,
) -> None:
    database.join_game(game.key, "My Name")
    response = testclient.post(
        f"/game/{game.key}/item/{game.items[0].key}",
        follow_redirects=False,
        cookies={"player_name": "My Name"},
        data={"game_key": game.key, "item_key": game.items[0].key, "vote": game.items[0].options[0].key},
    )
    assert response.status_code == 303
    assert response.headers["Location"] == f"/game/{game.key}/item/{game.items[1].key}"


def post_play_item_vote_should_return_303_to_results_if_all_items_have_been_voted(
    testclient: TestClient,
    database: Database,
    game: Game,
) -> None:
    database.join_game(game.key, "My Name")
    database.vote("My Name", game.key, game.items[0].key, game.items[0].options[0].key)
    response = testclient.post(
        f"/game/{game.key}/item/{game.items[1].key}",
        follow_redirects=False,
        cookies={"player_name": "My Name"},
        data={"game_key": game.key, "item_key": game.items[1].key, "vote": game.items[1].options[0].key},
    )
    assert response.status_code == 303
    assert response.headers["Location"] == f"/game/{game.key}/results"
