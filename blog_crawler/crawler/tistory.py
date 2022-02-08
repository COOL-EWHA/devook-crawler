from blog_crawler.utils import remove_escape
from blog_crawler.crawler.base import BlogCrawler


class TistoryCrawler(BlogCrawler):
    def __init__(self, url):
        BlogCrawler.__init__(self, url)

    @property
    def content(self):
        return remove_escape(
            (
                self._soup.select_one("div.entry-content")
                or self._soup.select_one("div.contents_style")
                or self._soup.select_one("div.article_view")
                or self._soup.select_one("article")
            ).get_text()
        )
