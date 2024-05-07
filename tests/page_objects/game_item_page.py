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
