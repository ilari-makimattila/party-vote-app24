from copy import deepcopy

from voting24.db.database import InMemoryDatabase
from voting24.game.game import Choice, Game, VoteItem

_default_choices = [
    Choice(key="hateit", text="🤮", value=-2),
    Choice(key="dislikeit", text="🤢", value=-1),
    Choice(key="neutral", text="🤷", value=0),
    Choice(key="likeit", text="🤩", value=1),
    Choice(key="loveit", text="😍", value=2),
    Choice(key="absolutefav", text="💖", value=4),
]

_hardcoded_eurovision24_game = Game(
    key="eurovision24",
    name="Eurovision 2024",
    css="""
h1 {
    padding: 1em 0;
    background: url(https://eurovision.tv/themes/custom/ebu_esc/html/public/assets/images/web-header-2023.gif);
    background-size: auto;
    background-size: auto 100%;
    margin: 0 auto;
    position: absolute;
    width: 100%;
    left: 0;
    top: 0;
    height: 3em;
}

.container {
    margin-top: 7em;
}
""",
    players=[],
    items=[
        VoteItem.new(
            "Croatia", "Baby Lasagna - Rim Tim Tagi Dim", _default_choices, "🇭🇷",
            "https://eurovision.tv/sites/default/files/styles/banner/public/media/image/2024-05/01-05.24%20Corinne%20Cumming%20-%20EBU%207966.jpg",
        ),
        VoteItem.new(
            "Cyprus", "Silia Kapsis - Liar", _default_choices, "🇨🇾",
            "https://eurovision.tv/sites/default/files/styles/banner/public/media/image/2024-05/01-05.24%20Corinne%20Cumming%20-%20EBU%207686.jpg",
        ),
        VoteItem.new(
            "Finland", "Windows95man - No Rules!", _default_choices, "🇫🇮",
            "https://eurovision.tv/sites/default/files/styles/banner/public/media/image/2024-05/01-05.24%20Corinne%20Cumming%20-%20EBU%208116.jpg",
        ),
        VoteItem.new(
            "France", "Slimane - Mon amour", _default_choices, "🇫🇷",
            "https://eurovision.tv/sites/default/files/styles/banner/public/media/image/2024-05/04.05.24%20Corinne%20Cumming%20-%20EBU%2013134.jpg",
        ),
        VoteItem.new(
            "Germany", "ISAAK - Always On The Run", _default_choices, "🇩🇪",
            "https://eurovision.tv/sites/default/files/styles/banner/public/media/image/2024-05/04.05.24%20Corinne%20Cumming%20-%20EBU%2012893_0.jpg",
        ),
        VoteItem.new(
            "Ireland", "Bambie Thug - Doomsday Blue", _default_choices, "🇮🇪",
            "https://eurovision.tv/sites/default/files/styles/banner/public/media/image/2024-05/01-05.24%20Corinne%20Cumming%20-%20EBU%207880.jpg",
        ),
        VoteItem.new(
            "Italy", "Angelina Mango - La noia", _default_choices, "🇮🇹",
            "https://eurovision.tv/sites/default/files/styles/banner/public/media/image/2024-05/04.05.24%20Corinne%20Cumming%20-%20EBU%2013287.jpg",
        ),
        VoteItem.new(
            "Lithuania", "Silvester Belt - Luktelk", _default_choices, "🇱🇹",
            "https://eurovision.tv/sites/default/files/styles/banner/public/media/image/2024-05/01-05.24%20Corinne%20Cumming%20-%20EBU%207747.jpg",
        ),
        VoteItem.new(
            "Luxembourg", "TALI - Fighter", _default_choices, "🇱🇺",
            "https://eurovision.tv/sites/default/files/styles/banner/public/media/image/2024-05/01-05.24%20Corinne%20Cumming%20-%20EBU%208493.jpg",
        ),
        VoteItem.new(
            "Portugal", "iolanda - Grito", _default_choices, "🇵🇹",
            "https://eurovision.tv/sites/default/files/styles/banner/public/media/image/2024-05/01-05.24%20Corinne%20Cumming%20-%20EBU%208458.jpg",
        ),
        VoteItem.new(
            "Serbia", "TEYA DORA - RAMONDA", _default_choices, "🇷🇸",
            "https://eurovision.tv/sites/default/files/styles/banner/public/media/image/2024-05/01-05.24%20Corinne%20Cumming%20-%20EBU%207704.jpg",
        ),
        VoteItem.new(
            "Slovenia", "Raiven - Veronika", _default_choices, "🇸🇮",
            "https://eurovision.tv/sites/default/files/styles/banner/public/media/image/2024-05/01-05.24%20Corinne%20Cumming%20-%20EBU%208104.jpg",
        ),
        VoteItem.new(
            "Spain", "Nebulossa - ZORRA", _default_choices, "🇪🇸",
            "https://eurovision.tv/sites/default/files/styles/banner/public/media/image/2024-05/04.05.24%20Corinne%20Cumming%20-%20EBU%2013155.jpg",
        ),
        VoteItem.new(
                "Sweden", "Marcus & Martinus - Unforgettable", _default_choices, "🇸🇪",
            "https://eurovision.tv/sites/default/files/styles/banner/public/media/image/2024-05/04.05.24%20Corinne%20Cumming%20-%20EBU%2013077.jpg",
        ),
        VoteItem.new(
            "Ukraine", "alyona alyona & Jerry Heil - Teresa & Maria", _default_choices, "🇺🇦",
            "https://eurovision.tv/sites/default/files/styles/banner/public/media/image/2024-05/01-05.24%20Corinne%20Cumming%20-%20EBU%207792.jpg",
        ),
        VoteItem.new(
            "United Kingdom", "Olly Alexander - Dizzy", _default_choices, "🇬🇧",
            "https://eurovision.tv/sites/default/files/styles/banner/public/media/image/2024-05/04.05.24%20Corinne%20Cumming%20-%20EBU%2012840.jpg",
        ),
    ],
)

hardcoded_datatabase = InMemoryDatabase(games={
    _hardcoded_eurovision24_game.key: deepcopy(_hardcoded_eurovision24_game),
})
