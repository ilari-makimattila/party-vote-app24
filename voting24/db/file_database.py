from pathlib import Path

from voting24.db.database import (
    ChoiceNotFoundError,
    Database,
    GameNotFoundError,
    PlayerAlreadyExistsError,
    PlayerNotFoundError,
    VoteItemNotFoundError,
)
from voting24.game.game import Game, Key, Name, Player


class FileDatabase(Database):
    def __init__(self, path: Path) -> None:
        self.path = path

    def save_game(self, game: Game) -> None:
        game_path = self.path / f"{game.key}.json"
        game_path.write_text(game.json())

    def load_game(self, key: Key) -> Game:
        game_path = self.path / f"{key}.json"
        if not game_path.exists():
            raise GameNotFoundError(key)
        game = Game.model_validate_json(game_path.read_text())
        game.players = self._load_players(game.key)
        return game

    def join_game(self, key: Key, player_name: Name, *, join_as_existing: bool = False) -> Player:
        game = self.load_game(key)
        if not join_as_existing and player_name in (player.name for player in game.players):
            raise PlayerAlreadyExistsError(game.name, player_name)
        player = Player.new(name=player_name)
        self._save_player(player, game)
        return player

    def vote(self, player_name: Name, game_key: Key, item_key: Key, vote_key: Key) -> None:
        game = self.load_game(game_key)
        item = next((item for item in game.items if item.key == item_key), None)
        if not item:
            raise VoteItemNotFoundError(item_key, game.name)
        if not next((option for option in item.options if option.key == vote_key), None):
            raise ChoiceNotFoundError(vote_key, item_key, game.name)
        for player in game.players:
            if player.name == player_name:
                player.votes[item_key] = vote_key
                self._save_player(player, game)
                break
        else:
            raise PlayerNotFoundError(player_name, game.name)

    def _save_player(self, player: Player, game: Game) -> None:
        players_dir = self.path / game.key
        if not players_dir.exists():
            players_dir.mkdir()
        player_path = players_dir / f"{player.name}.json"
        player_path.write_text(player.json())

    def _load_players(self, game_key: Key) -> list[Player]:
        players_dir = self.path / game_key
        if not players_dir.exists():
            return []
        return [Player.model_validate_json(player_path.read_text()) for player_path in players_dir.glob("*.json")]
