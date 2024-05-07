from bs4 import Tag
from fastapi.testclient import TestClient

from tests.page_objects.base import PageBase
from voting24.game.game import Key


class GamePage(PageBase):
    @classmethod
    def open(cls, testclient: TestClient, game_key: Key) -> "GamePage":
        return cls(testclient.get(f"/game/{game_key}"))

    def name(self) -> str:
        h1 = self.css.select_one("h1")
        assert h1
        return str(h1.text)

    def join_form_fields(self) -> dict[str, Tag]:
        form = self.join_form()
        return {inp.attrs["name"]: inp for inp in form.select("input")}

    def join_form(self) -> Tag:
        form = self.css.select_one("#join-form")
        assert form
        return form
