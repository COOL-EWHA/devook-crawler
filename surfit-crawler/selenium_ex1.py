# 데이터 1개에 대한 크롤러
# 크롤링 항목 : URL, 제목, Description, 태그(태그 2개)
from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Chrome("./chromedriver")
driver.implicitly_wait(3)

url = "https://www.surfit.io/explore/develop/web-dev"
driver.get(url)
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

title = soup.find("div", "ct-title")  # url, title
# title.text
# title.contents[0].attrs['href']
print('title: ', title.text)
print('\nurl: ', title.contents[0].attrs['href'])

description = soup.find("div", "ct-text")  # description
# description.text
print('\ndescription: ', description.text)

tags = soup.find("div", "ct-tag")  # tags
# tags.contents[0].text
# tags.contents[1].text
print('\ntag: ', tags.contents[0].text)
print('\ntag: ', tags.contents[1].text)


