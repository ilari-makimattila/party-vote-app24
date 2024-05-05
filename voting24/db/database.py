from abc import ABC, abstractmethod

from voting24.game.game import Game, Key


class Database(ABC):
    @abstractmethod
    def save_game(self, game: Game) -> None:
        raise NotImplementedError

    @abstractmethod
    def load_game(self, key: Key) -> Game:
        raise NotImplementedError


class InMemoryDatabase(Database):
    def __init__(self, games: dict[Key, Game] | None = None) -> None:
        self.games: dict[Key, Game] = games or {}

    def save_game(self, game: Game) -> None:
        self.games[game.key] = game

    def load_game(self, key: Key) -> Game:
        return self.games[key]
