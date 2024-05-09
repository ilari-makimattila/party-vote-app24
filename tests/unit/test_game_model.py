import pytest
from pydantic import ValidationError

from voting24.game.game import Choice, Game, Player, VoteItem


def test_game_can_be_created() -> None:
    game = Game.new(name="name")
    assert game


def test_game_key_will_be_generated_from_name() -> None:
    game = Game.new(name="Is this correct?   Not really.")
    assert game.key == "is-this-correct-not-really"


def test_game_key_can_be_provided() -> None:
    game = Game.new(name="x", key="this-is-correct")
    assert game.key == "this-is-correct"


def test_game_key_must_match_regex() -> None:
    with pytest.raises(ValidationError):
        Game.new(name="x", key="This should fail")


def empty_game_points_should_be_empty() -> None:
    game = Game(key="key", name="name", items=[], players=[])
    assert game.points() == {}


def game_vote_item_key_should_be_unique_by_key() -> None:
    game = Game.new(name="name")
    with pytest.raises(ValidationError):
        game.items = [
            VoteItem(key="key", title="text", text="text", options=[]),
            VoteItem(key="key", title="text2", text="text2", options=[]),
        ]


def game_vote_item_choices_should_be_unique_by_key() -> None:
    vote_item = VoteItem(key="key", title="text", text="text", options=[])
    with pytest.raises(ValidationError):
        vote_item.options = [
            Choice(key="key", text="text", value=1),
            Choice(key="key", text="text", value=2),
        ]


def game_points_should_be_calculated() -> None:
    game = Game(
        key="key",
        name="name",
        items=[
            VoteItem(key="itemkey", title="text", text="text", options=[
                Choice(key="choicekey1", text="text", value=1),
                Choice(key="choicekey2", text="text", value=2),
                Choice(key="choicekey3", text="text", value=3),
            ]),
        ],
        players=[
            Player(name="name", votes={
                "itemkey": "choicekey1",
            }),
            Player(name="name", votes={
                "itemkey": "choicekey2",
            }),
        ],
    )
    assert game.points() == {
        game.items[0]: 3,
    }


def game_points_should_be_calculated_when_all_players_have_not_voted() -> None:
    game = Game(
        key="key",
        name="name",
        items=[
            VoteItem(key="itemkey", title="text", text="text", options=[
                Choice(key="choicekey1", text="text", value=1),
                Choice(key="choicekey2", text="text", value=2),
                Choice(key="choicekey3", text="text", value=3),
            ]),
        ],
        players=[
            Player(name="name", votes={
                "itemkey": "choicekey1",
            }),
            Player(name="name", votes={}),
        ],
    )
    assert game.points() == {
        game.items[0]: 1,
    }


def game_points_should_be_calculated_when_items_have_been_not_voted() -> None:
    game = Game(
        key="key",
        name="name",
        items=[
            VoteItem(key="itemkey", title="text", text="text", options=[
                Choice(key="choicekey1", text="text", value=1),
                Choice(key="choicekey2", text="text", value=2),
            ]),
            VoteItem(key="itemkey2", title="text", text="text", options=[
                Choice(key="choicekey1", text="text", value=1),
                Choice(key="choicekey2", text="text", value=2),
            ]),

        ],
        players=[
            Player(name="name", votes={
                "itemkey2": "choicekey2",
            }),
            Player(name="name", votes={}),
        ],
    )
    assert game.points() == {
        game.items[0]: 0,
        game.items[1]: 2,
    }


def game_next_unvoted_item_should_return_first_unvoted_item() -> None:
    game = Game(
        key="key",
        name="name",
        items=[
            VoteItem(key="itemkey", title="text", text="text", options=[
                Choice(key="choicekey1", text="text", value=1),
                Choice(key="choicekey2", text="text", value=2),
            ]),
            VoteItem(key="itemkey2", title="text", text="text", options=[
                Choice(key="choicekey1", text="text", value=1),
                Choice(key="choicekey2", text="text", value=2),
            ]),

        ],
        players=[
            Player(name="name 1", votes={
                "itemkey": "choicekey2",
            }),
            Player(name="name 2", votes={}),
        ],
    )
    assert game.next_unvoted_item("name 1") == "itemkey2"
    assert game.next_unvoted_item("name 2") == "itemkey"


def game_next_unvoted_item_should_return_none_if_all_items_have_votes() -> None:
    game = Game(
        key="key",
        name="name",
        items=[
            VoteItem(key="itemkey", title="text", text="text", options=[
                Choice(key="choicekey1", text="text", value=1),
                Choice(key="choicekey2", text="text", value=2),
            ]),
            VoteItem(key="itemkey2", title="text", text="text", options=[
                Choice(key="choicekey1", text="text", value=1),
                Choice(key="choicekey2", text="text", value=2),
            ]),

        ],
        players=[
            Player(name="name 1", votes={
                "itemkey": "choicekey2",
                "itemkey2": "choicekey2",
            }),
        ],
    )
    assert game.next_unvoted_item("name 1") is None


def game_votes_should_list_all_votes_with_players() -> None:
    players = [
        Player(name="name 1", votes={
            "itemkey": "choicekey1",
        }),
        Player(name="name 2", votes={
            "itemkey": "choicekey2",
            "itemkey2": "choicekey2",
        }),
    ]
    game = Game(
        key="key",
        name="name",
        items=[
            VoteItem(key="itemkey", title="text", text="text", options=[
                Choice(key="choicekey1", text="text", value=1),
                Choice(key="choicekey2", text="text", value=2),
            ]),
            VoteItem(key="itemkey2", title="text", text="text", options=[
                Choice(key="choicekey1", text="text", value=1),
                Choice(key="choicekey2", text="text", value=2),
            ]),
            VoteItem(key="itemkey3", title="text", text="text", options=[
                Choice(key="choicekey1", text="text", value=1),
                Choice(key="choicekey2", text="text", value=2),
            ]),
        ],
        players=players,
    )
    assert game.votes() == {
        game.items[0]: [players[0], players[1]],
        game.items[1]: [players[1]],
        game.items[2]: [],
    }


def game_previous_item_should_be_none_for_first_item() -> None:
    game = Game(
        key="key",
        name="name",
        items=[
            VoteItem(key="itemkey", title="text", text="text", options=[]),
        ],
        players=[],
    )
    assert game.previous_item(game.items[0]) is None


def game_previous_item_should_the_previous_item() -> None:
    game = Game(
        key="key",
        name="name",
        items=[
            VoteItem(key="itemkey", title="text", text="text", options=[]),
            VoteItem(key="itemkey2", title="text", text="text", options=[]),
        ],
        players=[],
    )
    assert game.previous_item(game.items[1]) == game.items[0]


def game_next_item_should_be_none_for_last_item() -> None:
    game = Game(
        key="key",
        name="name",
        items=[
            VoteItem(key="itemkey", title="text", text="text", options=[]),
        ],
        players=[],
    )
    assert game.next_item(game.items[0]) is None


def game_next_item_should_the_next_item() -> None:
    game = Game(
        key="key",
        name="name",
        items=[
            VoteItem(key="itemkey", title="text", text="text", options=[]),
            VoteItem(key="itemkey2", title="text", text="text", options=[]),
        ],
        players=[],
    )
    assert game.next_item(game.items[0]) == game.items[1]
