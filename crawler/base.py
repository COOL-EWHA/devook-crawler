import urllib.request
from bs4 import BeautifulSoup


class BlogCrawler:
    def __init__(self, url):
        self._soup = BeautifulSoup(urllib.request.urlopen(url).read(), "html.parser")

    @property
    def info(self):
        return {
            "title": self.title,
            "description": self.description,
            "image": self.image,
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
