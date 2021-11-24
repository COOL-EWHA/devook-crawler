from crawler.base import BlogCrawler
from crawler.tistory import TistoryCrawler
from crawler.velog import VelogCrawler
from urllib.error import HTTPError


def lambda_handler(event, context):
    url = event["url"]

    base_crawler = BlogCrawler(url)
    print(base_crawler.info)

    try:
        if "velog.io" in url:
            crawler = VelogCrawler(url)
        elif "tistory.com" in url:
            crawler = TistoryCrawler(url)
        else:
            crawler = {"content": ""}

        print(crawler.content)

    except HTTPError:
        pass
        return
