from utils import remove_escape
from crawler.base import BlogCrawler


class VelogCrawler(BlogCrawler):
    def __init__(self, url):
        BlogCrawler.__init__(self, url)

    @property
    def content(self):
        return remove_escape(
            (
                self._soup.select_one("#root div.sc-cIShpX.cUTnDC")
                or self._soup.select_one("#root div.sc-bXGyLb.eLTqCr")
            ).get_text()
        )
