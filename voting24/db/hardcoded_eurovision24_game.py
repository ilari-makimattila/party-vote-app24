from copy import deepcopy

from voting24.db.database import InMemoryDatabase
from voting24.game.game import Choice, Game, VoteItem

_default_choices = [
    Choice(key="hateit", text="I hate it", value=-2),
    Choice(key="dislikeit", text="I dislike it", value=-1),
    Choice(key="neutral", text="I don't know", value=0),
    Choice(key="likeit", text="I like it", value=1),
    Choice(key="loveit", text="I love it", value=2),
]

_hardcoded_eurovision24_game = Game(
    key="eurovision24",
    name="Eurovision 2024",
    players=[],
    items=[
        VoteItem.new("Croatia", "Baby Lasagna - Rim Tim Tagi Dim", _default_choices, "🇭🇷"),
        VoteItem.new("Cyprus", "Silia Kapsis - Liar", _default_choices, "🇨🇾"),
        VoteItem.new("Finland", "Windows95man - No Rules!", _default_choices, "🇫🇮"),
        VoteItem.new("France", "Slimane - Mon amour", _default_choices, "🇫🇷"),
        VoteItem.new("Germany", "ISAAK - Always On The Run", _default_choices, "🇩🇪"),
        VoteItem.new("Ireland", "Bambie Thug - Doomsday Blue", _default_choices, "🇮🇪"),
        VoteItem.new("Italy", "Angelina Mango - La noia", _default_choices, "🇮🇹"),
        VoteItem.new("Lithuania", "Silvester Belt - Luktelk", _default_choices, "🇱🇹"),
        VoteItem.new("Luxembourg", "TALI - Fighter", _default_choices, "🇱🇺"),
        VoteItem.new("Portugal", "iolanda - Grito", _default_choices, "🇵🇹"),
        VoteItem.new("Serbia", "TEYA DORA - RAMONDA", _default_choices, "🇷🇸"),
        VoteItem.new("Slovenia", "Raiven - Veronika", _default_choices, "🇸🇮"),
        VoteItem.new("Spain", "Nebulossa - ZORRA", _default_choices, "🇪🇸"),
        VoteItem.new("Sweden", "Marcus & Martinus - Unforgettable", _default_choices, "🇸🇪"),
        VoteItem.new("Ukraine", "alyona alyona & Jerry Heil - Teresa & Maria", _default_choices, "🇺🇦"),
        VoteItem.new("United Kingdom", "Olly Alexander - Dizzy", _default_choices, "🇬🇧"),
    ],
)

hardcoded_datatabase = InMemoryDatabase(games={
    _hardcoded_eurovision24_game.key: deepcopy(_hardcoded_eurovision24_game),
})
