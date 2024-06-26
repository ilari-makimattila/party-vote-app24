from bs4 import Tag

from tests.page_objects.base import PageBase


class GameItemPage(PageBase):
    def vote_form(self) -> Tag:
        form = self.css.select_one("#vote-form")
        assert form
        return form

    def vote_form_fields(self) -> dict[str, Tag]:
        form = self.vote_form()
        return {inp.attrs["name"]: inp for inp in form.select("input")}

    def next_item_link(self) -> Tag | None:
        return self.css.select_one(".goto.next-item")

    def previous_item_link(self) -> Tag | None:
        return self.css.select_one(".goto.previous-item")

    def results_link(self) -> Tag:
        link = self.css.select_one(".goto.results")
        assert link
        return link

    def vote_item_icon(self) -> Tag | None:
        return self.css.select_one(".item-icon")

    def vote_item_image(self) -> Tag | None:
        return self.css.select_one(".item-image")
