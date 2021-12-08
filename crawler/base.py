import urllib.request
from bs4 import BeautifulSoup

from utils import remove_escape


class BlogCrawler:
    def __init__(self, url):
        headers = {"User-Agent": "Mozilla/5.0"}
        req = urllib.request.Request(url, headers=headers)
        self._soup = BeautifulSoup(urllib.request.urlopen(req).read(), "html.parser")

    @property
    def info(self):
        return {
            "title": self.title,
            "description": self.description,
            "image": self.image,
            "content": self.content,
        }

    @property
    def title(self):
        tag = self._soup.find("meta", property="og:title")
        return tag["content"] if tag else ""

    @property
    def description(self):
        tag = self._soup.find("meta", property="og:description")
        return tag["content"] if tag else ""

    @property
    def image(self):
        tag = self._soup.find("meta", property="og:image")
        return tag["content"] if tag else ""

    @property
    def content(self):
        # return remove_escape((self._soup.select_one("body")).get_text() or "")
        return remove_escape(
            (
                self._soup.select_one("article")
                or self._soup.select_one("main")
                or self._soup.select_one("body")
            ).get_text()
            or ""
        )
