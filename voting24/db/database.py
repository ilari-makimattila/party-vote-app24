from abc import ABC, abstractmethod

from voting24.game.game import Game, Key, Player


class DatabaseError(Exception):
    pass


class GameNotFoundError(DatabaseError):
    def __init__(self, key: Key) -> None:
        super().__init__(f"Game {key} not found")
        self.key = key


class PlayerAlreadyExistsError(DatabaseError):
    def __init__(self, name: str, player_name: str) -> None:
        super().__init__(f"Player {player_name} already exists in game {name}")
        self.name = name
        self.player_name = player_name


class PlayerNotFoundError(DatabaseError):
    def __init__(self, player_name: str, game_name: str) -> None:
        super().__init__(f"Player {player_name} not found in game {game_name}")
        self.player_name = player_name
        self.game_name = game_name


class Database(ABC):
    @abstractmethod
    def save_game(self, game: Game) -> None:
        raise NotImplementedError

    @abstractmethod
    def load_game(self, key: Key) -> Game:
        raise NotImplementedError

    @abstractmethod
    def join_game(self, key: Key, player_name: str, *, join_as_existing: bool = False) -> None:
        raise NotImplementedError

    @abstractmethod
    def vote(self, player_name: str, game_key: Key, item_key: Key, vote_key: Key) -> None:
        raise NotImplementedError


class InMemoryDatabase(Database):
    def __init__(self, games: dict[Key, Game] | None = None) -> None:
        self.games: dict[Key, Game] = games or {}

    def save_game(self, game: Game) -> None:
        self.games[game.key] = game

    def load_game(self, key: Key) -> Game:
        try:
            return self.games[key]
        except KeyError:
            raise GameNotFoundError(key) from None

    def join_game(self, key: Key, player_name: str, *, join_as_existing: bool = False) -> None:
        game = self.load_game(key)
        if not join_as_existing and player_name in (player.name for player in game.players):
            raise PlayerAlreadyExistsError(game.name, player_name)
        self.games[key].players.append(Player.new(name=player_name))

    def vote(self, player_name: str, game_key: Key, item_key: Key, vote_key: Key) -> None:
        game = self.load_game(game_key)
        for player in game.players:
            if player.name == player_name:
                player.votes[item_key] = vote_key
                break
        else:
            raise PlayerNotFoundError(player_name, game.name)
