from bs4 import BeautifulSoup
from httpx import Response


class PageBase:
    def __init__(self, response: Response) -> None:
        html = response.text
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
