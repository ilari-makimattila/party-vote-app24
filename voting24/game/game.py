import re
from typing import Annotated, TypeVar

from pydantic import AfterValidator, Field

from voting24.game.model import Model

GAME_KEY_REGEX = re.compile(r"^[\w-]+$")
GAME_NAME_REGEX = re.compile(r"^[\w\- ]+$")
GAME_KEY_SANITIZE_REGEX = re.compile(r"[^\w-]+")

T = TypeVar("T")


def _unique_list_validator(items: list[T]) -> list[T]:
    if len(set(items)) != len(items):
        message = "items must be unique"
        raise ValueError(message)
    return items


Key = Annotated[str, Field(pattern=GAME_KEY_REGEX, min_length=1, max_length=32)]
Name = Annotated[str, Field(pattern=GAME_NAME_REGEX, min_length=1, max_length=32)]
Text = Annotated[str, Field(min_length=0)]
Char = Annotated[str, Field(min_length=1, max_length=2)]  # you know, some emojis have a lot of character
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
    icon: Char | None = None
    title: Text
    text: Text
    image_url: Text | None = None
    options: UniqueList[Choice]

    @classmethod
    def new(  # noqa: PLR0913  # this is a convenience constsructor
        cls,
        title: Text,
        text: Text,
        options: list[Choice],
        icon: Char | None = None,
        image_url: Text | None = None,
    ) -> "VoteItem":
        return VoteItem(
            key=GAME_KEY_SANITIZE_REGEX.sub("-", title.lower()).strip("-"),
            title=title,
            text=text,
            icon=icon,
            image_url=image_url,
            options=options,
        )

    def __hash__(self) -> int:
        return hash(self.key)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, VoteItem) and self.key == other.key


class Player(Model):
    name: Name
    votes: dict[Key, Key]

    @classmethod
    def new(cls, name: Text) -> "Player":
        return Player(name=name, votes={})


class Game(Model):
    key: Key
    name: Text
    css: Text | None = None
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
                next(choice.value for choice in item.options if choice.key == itemkey)
                for itemkey
                in [player.votes[item.key] for player in players]
            )
            for item, players
            in self.votes().items()
        }

    def votes(self) -> dict[VoteItem, list[Player]]:
        return {
            item: [
                player
                for player
                in self.players
                if player.votes.get(item.key)
            ]
            for item
            in self.items
        }

    def next_unvoted_item(self, player_name: Name) -> Key | None:
        votes = next((player.votes for player in self.players if player.name == player_name), {})
        for item in self.items:
            if item.key not in votes:
                return item.key
        return None

    def previous_item(self, item: VoteItem) -> VoteItem | None:
        index = self.items.index(item)
        if index > 0:
            return self.items[index - 1]
        return None

    def next_item(self, item: VoteItem) -> VoteItem | None:
        index = self.items.index(item)
        if index < len(self.items) - 1:
            return self.items[index + 1]
        return None

    def player(self, player_name: Name) -> Player | None:
        return next((player for player in self.players if player.name == player_name), None)
