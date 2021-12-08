from crawler.base import BlogCrawler
from crawler.medium import MediumCrawler
from crawler.tistory import TistoryCrawler
from crawler.velog import VelogCrawler
from urllib.error import HTTPError


def lambda_handler(event, context):
    url = event["url"]


    try:
        if "velog.io" in url:
            crawler = VelogCrawler(url)
        elif "tistory.com" in url:
            crawler = TistoryCrawler(url)
        elif "medium.com" in url:
            crawler = MediumCrawler(url)
        else:
            crawler = BlogCrawler(url)

        return crawler.info.copy()

    except HTTPError:
        pass
        return

