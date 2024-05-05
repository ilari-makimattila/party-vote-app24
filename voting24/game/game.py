from voting24.game.model import Model

Key = str
Value = int


class Choice(Model):
    key: Key
    text: str
    value: Value


class VoteItem(Model):
    key: Key
    text: str
    options: list[Choice]

    def __hash__(self) -> int:
        return hash(self.key)


class Player(Model):
    name: str
    votes: dict[Key, Key]


class Game(Model):
    key: Key
    name: str
    items: list[VoteItem]
    players: list[Player]

    def points(self) -> dict[VoteItem, Value]:
        return {
            item: sum(
                choice.value
                for choice
                in item.options
                if choice.key in (
                    player.votes.get(item.key)
                    for player
                    in self.players
                )
            )
            for item
            in self.items
        }
