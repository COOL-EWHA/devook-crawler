import time

from crawler.utils.utils import (
    loads_a_web_page_in_the_current_session,
    set_beautifulsoup,
)

from crawler.utils.parsers import (
    parse_title_tistory,
)


def one_cycle_of_crawling_tistory(driver, url, posts, index):
    soup = convert_driver_to_beautifulsoup_with_web_page_scroll(driver, url)

    # data parsing
    parse_title_tistory(soup=soup, tag_name="strong", class_name="tit_post", posts=posts, index=index)


def convert_driver_to_beautifulsoup_with_web_page_scroll(driver, url):
    loads_a_web_page_in_the_current_session(driver=driver, url=url)
    web_page_scroll(driver=driver)
    return set_beautifulsoup(driver=driver)


def web_page_scroll(driver):

    SCROLL_PAUSE_TIME = 5

    last_height = driver.execute_script("return document.body.scrollHeight")

    for i in range(0, 1000):  # 크롤링할 데이터 개수 조절
        # scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight-50);")
        time.sleep(SCROLL_PAUSE_TIME)

        new_height = driver.execute_script("return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height


def append_data_tistory(titles):
    items = []
    for i, title in enumerate(titles):
        data = [title]
        items.append(data)
    return items
