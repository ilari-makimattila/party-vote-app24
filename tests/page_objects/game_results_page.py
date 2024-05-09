from bs4 import Tag
from fastapi.testclient import TestClient

from tests.page_objects.base import PageBase
from voting24.game.game import Key, Text, Value


class GameResultsPage(PageBase):
    @classmethod
    def open(cls, testclient: TestClient, game_key: Key) -> "GameResultsPage":
        return cls(testclient.get(f"/game/{game_key}/results"))

    def name(self) -> str:
        h1 = self.css.select_one("h1")
        assert h1
        return str(h1.text)

    def results(self) -> list[tuple[Text, Value]]:
        result_tags = self.css.select("#game-results .result")
        assert result_tags
        results = []

        for result_tag in result_tags:
            title = result_tag.select_one(".title .item-title")
            assert title
            score = result_tag.select_one(".score")
            assert score
            results.append((title.text.strip(), int(score.text)))

        return results

    def first_item_link(self) -> Tag:
        first_item_link = self.css.select_one(".goto.first-item")
        assert first_item_link
        return first_item_link

    def all_item_links(self) -> list[Tag]:
        item_links = self.css.select(".goto.item")
        assert item_links
        return item_links

    def result_icons(self) -> list[Tag]:
        result_icons = self.css.select(".item-icon")
        assert result_icons
        return result_icons
