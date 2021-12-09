from urllib.error import HTTPError

from crawler.base import BlogCrawler
from crawler.medium import MediumCrawler
from crawler.tistory import TistoryCrawler
from crawler.velog import VelogCrawler


def lambda_handler(event, context):
    url = event["url"]

    base_crawler = BlogCrawler(url)
    print(base_crawler.info)

    try:
        if "velog.io" in url:
            crawler = VelogCrawler(url)
        elif "tistory.com" in url:
            crawler = TistoryCrawler(url)
        elif "medium.com" in url:
            crawler = MediumCrawler(url)
        else:
            crawler = {"content": ""}

        print("Contents size : %d\n" % len(crawler.content))
        return crawler.content

    except HTTPError:
        pass
        return
