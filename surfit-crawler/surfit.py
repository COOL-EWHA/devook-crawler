"""
Surfit Crawler

1. get post list page html from Surfit
2. parse url, title, description from html
3. insert url, title, description, category into mysql
"""
import time
import MySQLdb
from selenium import webdriver
from bs4 import BeautifulSoup

surfit_url_list = ["https://www.surfit.io/explore/develop/general-dev",
                   "https://www.surfit.io/explore/develop/web-dev",
                   "https://www.surfit.io/explore/develop/javascript",
                   "https://www.surfit.io/explore/develop/react",
                   "https://www.surfit.io/explore/develop/vuejs",
                   "https://www.surfit.io/explore/develop/angular",
                   "https://www.surfit.io/explore/develop/nodejs",
                   "https://www.surfit.io/explore/develop/java",
                   "https://www.surfit.io/explore/develop/python",
                   "https://www.surfit.io/explore/develop/php",
                   "https://www.surfit.io/explore/develop/infra-structure",
                   "https://www.surfit.io/explore/develop/database",
                   "https://www.surfit.io/explore/develop/android",
                   "https://www.surfit.io/explore/develop/ios",
                   "https://www.surfit.io/explore/develop/git",
                   "https://www.surfit.io/explore/develop/bigdata-ai-ml"]

category_list = ["일반 개발", "웹 개발", "Javascript", "React",
                 "Vue.js", "Angular", "Node.js", "Java",
                 "Python", "PHP", "Infra Structure", "Database",
                 "Android", "iOS", "Git", "빅데이터/AI/머신러닝"]


def set_chrome_driver():
    driver = webdriver.Chrome("./chromedriver")
    driver.implicitly_wait(3)
    return driver


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
    return BeautifulSoup(html, 'html.parser')


def parse_url_title_description(soup, tag_name, class_name, urls, titles, descriptions, category, index):
    items = soup.find_all(tag_name, class_name)

    for item in items:
        urls.append(item.find("div", "ct-title").contents[0].attrs['href'])
        titles.append(item.find("div", "ct-title").text)
        descriptions.append(item.find("div", "ct-text").text)
        category.append(category_list[index])


def append_data(urls, titles, descriptions, category):
    items = []
    for i, url in enumerate(urls):
        data = (url, titles[i], descriptions[i], category[i])
        items.append(data)
    return items


def insert_into_database(items):
    conn = MySQLdb.connect(
        user="root",
        passwd="cool",
        host="127.0.0.1",
        db="devook_db"
    )
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS post")  # 해당 테이블이 이미 존재할 경우 삭제
    cursor.execute(
        "CREATE TABLE post "
        "(id            int AUTO_INCREMENT PRIMARY KEY, "
        "url            text, "
        "title          text, "
        "description    text, "
        "category       text)"
    )  # 새로운 테이블 생성

    sql = "INSERT INTO post(url, title, description, category) VALUES(%s, %s, %s, %s)"
    for item in items:
        values = (item[0], item[1], item[2], item[3])
        cursor.execute(sql, values)

    conn.commit()
    conn.close()


def surfit_crawl():
    driver = set_chrome_driver()

    urls = []
    titles = []
    descriptions = []
    category = []
    for i, surfit_url in enumerate(surfit_url_list):
        loads_a_web_page_in_the_current_session(driver, surfit_url)
        web_page_scroll(driver)
        soup = set_beautifulsoup(driver)
        parse_url_title_description(soup, "div", "ct-item base", urls, titles, descriptions, category, i)
        parse_url_title_description(soup, "div", "ct-item text", urls, titles, descriptions, category, i)

    items = append_data(urls, titles, descriptions, category)
    insert_into_database(items)

    driver.close()


if __name__ == '__main__':
    surfit_crawl()
