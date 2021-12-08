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
        return self._soup.find("meta", property="og:title")["content"]

    @property
    def description(self):
        return self._soup.find("meta", property="og:description")["content"]

    @property
    def image(self):
        return self._soup.find("meta", property="og:image")["content"]

    @property
    def content(self):
        return remove_escape((self._soup.select_one("body")).get_text() or "")