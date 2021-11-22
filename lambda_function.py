from crawler.velog import VelogCrawler


def lambda_handler(event, context):
    url = event["url"]

    # base_crawler = BlogCrawler(url)
    velog_crawler = VelogCrawler(url)
    print(velog_crawler.content)
