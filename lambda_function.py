from crawler.base import BlogCrawler
from crawler.medium import MediumCrawler
from crawler.tistory import TistoryCrawler
from crawler.velog import VelogCrawler
from urllib.error import HTTPError


def lambda_handler(event, context):
    url = event["url"]

    base_crawler = BlogCrawler(url)
    ret = base_crawler.info.copy()

    try:
        if "velog.io" in url:
            crawler = VelogCrawler(url)
        elif "tistory.com" in url:
            crawler = TistoryCrawler(url)
        elif "medium.com" in url:
            crawler = MediumCrawler(url)
        else:
            crawler = {"content": ""}

        ret['content'] = crawler.content

    except HTTPError:
        pass
        return

    print(ret)