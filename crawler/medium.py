from utils import remove_escape
from crawler.base import BlogCrawler


class MediumCrawler(BlogCrawler):
    def __init__(self, url):
        BlogCrawler.__init__(self, url)

    @property
    def content(self):
        return remove_escape((self._soup.select_one("article")).get_text())
