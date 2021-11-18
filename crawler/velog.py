from .base import BlogCrawler


class VelogCrawler(BlogCrawler):
    def __init__(self, url):
        BlogCrawler.__init__(self, url)

    @property
    def content(self):
        return (
            self._soup.find("div", id="root")
            .find("div", class_=["sc-cIShpX", "cUTnDC", "sc-bXGyLb", "eLTqCr"])
            .text.replace("\n", " ")
        )
