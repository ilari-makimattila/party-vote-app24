from fastapi.testclient import TestClient

from tests.page_objects.base import PageBase
from voting24.game.game import Key


class GameResultsPage(PageBase):
    @classmethod
    def open(cls, testclient: TestClient, game_key: Key) -> "GameResultsPage":
        return cls(testclient.get(f"/game/{game_key}/results"))

    def name(self) -> str:
        h1 = self.css.select_one("h1")
        assert h1
        return str(h1.text)
