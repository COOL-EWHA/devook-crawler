# CursorPagination 적용된 모든 데이터 크롤링
# 크롤링 항목 : URL, 제목, Description, 태그(대표 카테고리 1개)
import time
from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome("./chromedriver")
driver.implicitly_wait(3)

url = "https://www.surfit.io/explore/develop/bigdata-ai-ml"
driver.get(url)

# 웹페이지 스크롤
# 방법1. scrollTo
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

# 데이터 개수 확인
item_base = soup.find_all("div", "ct-item base")
item_text = soup.find_all("div", "ct-item text")
print(len(item_base) + len(item_text))

# 모든 데이터의 title 출력 확인
# titles = soup.find_all("div", "ct-title")
# print('total title: ', len(titles))

# for title in titles:
#     print(title.text)
