from bs4 import BeautifulSoup, Tag
from fastapi.testclient import TestClient

from voting24.game.game import Key


class GamePage:
    @classmethod
    def open(cls, testclient: TestClient, game_key: Key) -> "GamePage":
        return cls(testclient.get(f"/game/{game_key}").text)

    def __init__(self, html: str) -> None:
        print(html)
        self.html = BeautifulSoup(html, "html.parser")
        css = self.html.css
        assert css
        self.css = css

    def title(self) -> str:
        t = self.html.title
        assert t
        assert t.string
        return t.string

    def name(self) -> str:
        h1 = self.css.select_one("h1")
        assert h1
        return str(h1.text)

    def join_form(self) -> dict[str, Tag]:
        form = self.css.select_one("#join-form")
        assert form
        return {inp.attrs["name"]: inp for inp in form.select("input")}
