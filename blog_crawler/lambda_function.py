from blog_crawler.crawler.base import BlogCrawler
from blog_crawler.crawler.medium import MediumCrawler
from blog_crawler.crawler.tistory import TistoryCrawler
from blog_crawler.crawler.velog import VelogCrawler
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

        return crawler.data

    except HTTPError:
        pass
        return
