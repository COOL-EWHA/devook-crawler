import time
import os

from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

from surfit_crawler.parsers import (
    parse_url_title_description,
    parse_categories,
    parse_urls,
)
from surfit_crawler.set_up_data import surfit_url_list, category_list


BASE_DIR = Path(__file__).resolve().parent.parent


def set_chrome_driver():
    # for local dev
    # options = Options()
    # options.headless = True
    # driver_path = os.path.join(BASE_DIR, "chromedriver")

    # for docker
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome("/usr/local/bin/chromedriver", options=chrome_options)
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


def append_data(urls, titles, descriptions, category):
    items = []
    for i, url in enumerate(urls):
        data = (url, titles[i], descriptions[i], category[i])  # tuple 생성
        items.append(data)
    return items


def convert_driver_to_beautifulsoup(driver, url):
    """
    Webdriver를 BeautifulSoup의 객체로 변경한다.
    :param driver: Webdriver
    :param url:
    :return: BeautifulSoup의 Object
    """
    loads_a_web_page_in_the_current_session(driver=driver, url=url)
    time.sleep(1)
    return set_beautifulsoup(driver=driver)


def get_surfit_dev_categories(driver, url):
    """
    Surfit 페이지의 개발 카테고리 목록을 반환한다.
    :param driver: Chrome webdriver
    :param url: driver로 연결할 페이지의 url
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
    카테고리 별 링크들을 크롤링하는 한번의 사이클이다.
    :param driver: Chrome webdriver
    :param url: 크롤링할 페이지의 url
    :return: url list
    """
    soup = convert_driver_to_beautifulsoup_with_web_page_scroll(driver=driver, url=url)
    return parse_urls(
        soup=soup, tag_name="div", class_name="ct-item base"
    ) + parse_urls(soup=soup, tag_name="div", class_name="ct-item text")


def get_urls_by_all_category(driver, urls_by_all_category_list):
    """
    :param driver: Chrome webdriver
    :param urls_by_all_category_list: 카테고리 별 url을 저장할 list
    """
    for url in surfit_url_list:
        urls = one_cycle_of_crawling_urls_by_category(driver=driver, url=url)
        urls_by_all_category_list.append(urls)
    print("완료")


def get_surfit_url_by_category_dict():
    """
    카테고리별 surfit 페이지 url을 dict 형태로 만든 후 반환한다.
    :return: dict
    """
    data = {}
    for i, category in enumerate(category_list):
        data[category] = surfit_url_list[i]
    return data
