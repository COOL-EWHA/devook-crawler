"""
Surfit Crawler
"""
import time
import MySQLdb
from selenium import webdriver
from bs4 import BeautifulSoup


def main():
    """
    1. get post list page html from Surfit
    2. parse url, title, description from html
    3. insert url, title, description, category into mysql
    """
    driver = webdriver.Chrome("./chromedriver")
    driver.implicitly_wait(3)

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

    category_list = [
        "일반 개발", "웹 개발", "Javascript", "React",
        "Vue.js", "Angular", "Node.js", "Java",
        "Python", "PHP", "Infra Structure", "Database",
        "Android", "iOS", "Git", "빅데이터/AI/머신러닝"]

    url = []
    title = []
    description = []
    category = []
    items = []
    for i, surfit_url in enumerate(surfit_url_list):
        driver.get(surfit_url)  # 현재 브라우저 세션에서 웹 페이지 로드

        # 웹페이지 스크롤
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        # BeaufitulSoup 적용
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # url, title, description, category 데이터 저장
        posts_b = soup.find_all("div", "ct-item base")
        posts_t = soup.find_all("div", "ct-item text")

        for b in posts_b:
            url.append(b.find("div", "ct-title").contents[0].attrs['href'])
            title.append(b.find("div", "ct-title").text)
            description.append(b.find("div", "ct-text").text)
            category.append(category_list[i])

        for t in posts_t:
            url.append(t.find("div", "ct-title").contents[0].attrs['href'])
            title.append(t.find("div", "ct-title").text)
            description.append(t.find("div", "ct-text").text)
            category.append(category_list[i])

    for i, url in enumerate(url):
        data = (url, title[i], description[i], category[i])
        items.append(data)

    # MySQL
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

    driver.close()


if __name__ == '__main__':
    main()
