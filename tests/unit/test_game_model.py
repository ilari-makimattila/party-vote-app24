from voting24.game.game import Choice, Game, Player, VoteItem


def empty_game_points_should_be_empty() -> None:
    game = Game(key="key", name="name", items=[], players=[])
    assert game.points() == {}


def game_points_should_be_calculated() -> None:
    game = Game(
        key="key",
        name="name",
        items=[
            VoteItem(key="itemkey", text="text", options=[
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
            VoteItem(key="itemkey", text="text", options=[
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
            VoteItem(key="itemkey", text="text", options=[
                Choice(key="choicekey1", text="text", value=1),
                Choice(key="choicekey2", text="text", value=2),
            ]),
            VoteItem(key="itemkey2", text="text", options=[
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
