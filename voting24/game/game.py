import re
from typing import Annotated, TypeVar

from pydantic import AfterValidator, Field

from voting24.game.model import Model

GAME_KEY_REGEX = re.compile(r"^[\w-]+$")
GAME_KEY_SANITIZE_REGEX = re.compile(r"[^\w-]+")

T = TypeVar("T")


def _unique_list_validator(items: list[T]) -> list[T]:
    if len(set(items)) != len(items):
        message = "items must be unique"
        raise ValueError(message)
    return items


Key = Annotated[str, Field(pattern=GAME_KEY_REGEX, min_length=1, max_length=32)]
Text = Annotated[str, Field(min_length=1, max_length=32)]
Value = int
UniqueList = Annotated[list[T], AfterValidator(_unique_list_validator)]


class Choice(Model):
    key: Key
    text: Text
    value: Value

    def __hash__(self) -> int:
        return hash(self.key)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Choice) and self.key == other.key


class VoteItem(Model):
    key: Key
    text: Text
    options: UniqueList[Choice]

    def __hash__(self) -> int:
        return hash(self.key)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, VoteItem) and self.key == other.key


class Player(Model):
    name: Text
    votes: dict[Key, Key]

    @classmethod
    def new(cls, name: Text) -> "Player":
        return Player(name=name, votes={})


class Game(Model):
    key: Key
    name: Text
    items: UniqueList[VoteItem]
    players: list[Player]

    @staticmethod
    def new(name: Text, key: Key | None = None) -> "Game":
        return Game(
            key=key or GAME_KEY_SANITIZE_REGEX.sub("-", name.lower()).strip("-"),
            name=name,
            items=[],
            players=[],
        )

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

    def next_unvoted_item(self, player_name: Text) -> Key:
        votes = next((player.votes for player in self.players if player.name == player_name), {})
        for item in self.items:
            if item.key not in votes:
                return item.key
        return self.items[0].key
