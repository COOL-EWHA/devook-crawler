import time
import os

from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

from crawler.utils.parsers import (
    parse_url_title_description,
    parse_categories,
    parse_urls,
)
from crawler.surfit.set_up_data import surfit_url_list, category_list


BASE_DIR = Path(__file__).resolve().parent.parent.parent


def set_chrome_driver():
    # for local dev
    options = Options()
    options.headless = True
    driver_path = os.path.join(BASE_DIR, "chromedriver")
    # driver = webdriver.Chrome(driver_path, options=options)
    driver = webdriver.Chrome(driver_path)

    # for docker
    # chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--headless')
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    # driver = webdriver.Chrome("/usr/local/bin/chromedriver", options=chrome_options)
    return driver


def initialize_jagged_list(list_name, list_length):
    for i in range(list_length):
        list_name.append([])


def loads_a_web_page_in_the_current_session(driver, url):
    driver.get(url)


def web_page_scroll(driver):
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def set_beautifulsoup(driver):
    html = driver.page_source
    return BeautifulSoup(html, "html.parser")


def convert_driver_to_beautifulsoup_with_web_page_scroll(driver, url):
    loads_a_web_page_in_the_current_session(driver=driver, url=url)
    web_page_scroll(driver=driver)
    return set_beautifulsoup(driver=driver)


def one_cycle_of_crawling(driver, url, posts, index):
    soup = convert_driver_to_beautifulsoup_with_web_page_scroll(driver, url)
    parse_url_title_description(
        soup=soup, tag_name="div", class_name="ct-item base", posts=posts, index=index
    )
    parse_url_title_description(
        soup=soup, tag_name="div", class_name="ct-item text", posts=posts, index=index
    )


def append_data(urls, titles, descriptions, category, image):
    items = []
    for i, url in enumerate(urls):
        data = (url, titles[i], descriptions[i], category[i], image[i])  # tuple ??????
        items.append(data)
    return items


def convert_driver_to_beautifulsoup(driver, url):
    """
    Webdriver??? BeautifulSoup??? ????????? ????????????.
    :param driver: Webdriver
    :param url:
    :return: BeautifulSoup??? Object
    """
    loads_a_web_page_in_the_current_session(driver=driver, url=url)
    time.sleep(1)
    return set_beautifulsoup(driver=driver)


def get_surfit_dev_categories(driver, url):
    """
    Surfit ???????????? ?????? ???????????? ????????? ????????????.
    :param driver: Chrome webdriver
    :param url: driver??? ????????? ???????????? url
    :return: list
    """
    soup = convert_driver_to_beautifulsoup(driver=driver, url=url)
    return parse_categories(
        soup=soup,
        find_tag_name="li",
        find_class_name="cate-level-1 is--open",
        find_all_tag_name="li",
        find_all_class_name="cate-level-2",
    )


def one_cycle_of_crawling_urls_by_category(driver, url):
    """
    ???????????? ??? ???????????? ??????????????? ????????? ???????????????.
    EC2??? ????????? ???????????? ??? ????????? ???????????? ???????????? ?????????.
    :param driver: Chrome webdriver
    :param url: ???????????? ???????????? url
    :return: url list
    """
    soup = convert_driver_to_beautifulsoup_with_web_page_scroll(driver=driver, url=url)
    return parse_urls(
        soup=soup, tag_name="div", class_name="ct-item base"
    ) + parse_urls(soup=soup, tag_name="div", class_name="ct-item text")


def get_urls_by_all_category(driver, urls_by_all_category_list):
    """
    :param driver: Chrome webdriver
    :param urls_by_all_category_list: ???????????? ??? url??? ????????? list
    """
    for url in surfit_url_list:
        urls = one_cycle_of_crawling_urls_by_category(driver=driver, url=url)
        urls_by_all_category_list.append(urls)
    print("??????")


def get_surfit_url_by_category_dict():
    """
    ??????????????? surfit ????????? url??? dict ????????? ?????? ??? ????????????.
    :return: dict
    """
    data = {}
    for i, category in enumerate(category_list):
        data[category] = surfit_url_list[i]
    return data
