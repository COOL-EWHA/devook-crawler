import time
import MySQLdb
from selenium   import webdriver
from bs4        import BeautifulSoup

from surfit_crawler.parsers import parse_url_title_description


def set_chrome_driver():
    driver = webdriver.Chrome("./chromedriver")
    driver.implicitly_wait(3)
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
    return BeautifulSoup(html, 'html.parser')


def convert_driver_to_beautifulsoup(driver, url):
    loads_a_web_page_in_the_current_session(driver=driver, url=url)
    web_page_scroll(driver=driver)
    return set_beautifulsoup(driver=driver)


def one_cycle_of_crawling(driver, url, posts, index):
    soup = convert_driver_to_beautifulsoup(driver, url)
    parse_url_title_description(soup=soup, tag_name="div", class_name="ct-item base", posts=posts, index=index)
    parse_url_title_description(soup=soup, tag_name="div", class_name="ct-item text", posts=posts, index=index)


def append_data(urls, titles, descriptions, category):
    items = []
    for i, url in enumerate(urls):
        data = (url, titles[i], descriptions[i], category[i])
        items.append(data)
    return items


def connect_db(user, passwd, host, db):
    return MySQLdb.connect(
        user=user,
        passwd=passwd,
        host=host,
        db=db
    )


def disconnect_db(conn):
    conn.commit()
    conn.close()


def insert_into_database(items, user, passwd, host, db):
    conn = connect_db(user=user, passwd=passwd, host=host, db=db)
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

    disconnect_db(conn=conn)
