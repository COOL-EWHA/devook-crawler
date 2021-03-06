"""
Surfit Crawler

1. get post list page html from Surfit
2. parse url, title, description from html
3. insert url, title, description, category into mysql
"""
from crawler.surfit.set_up_data import surfit_url_list
from crawler.utils.utils import (
    set_chrome_driver,
    append_data,
    initialize_jagged_list,
    one_cycle_of_crawling, one_cycle_of_crawling_urls_by_category,
)
from crawler.utils.utils_db import insert_into_database
from crawler.utils.utils_csv import save_to_csv
from crawler.surfit.set_up_data import category_list


def surfit_crawler_with_db():
    driver = set_chrome_driver()

    posts = []
    initialize_jagged_list(list_name=posts, list_length=4)

    for i, surfit_url in enumerate(surfit_url_list):
        one_cycle_of_crawling(driver, surfit_url, posts, i)

    items = append_data(
        urls=posts[0], titles=posts[1], descriptions=posts[2], category=posts[3]
    )
    insert_into_database(
        items=items, user="root", passwd="cool", host="127.0.0.1", db="test_db"
    )

    driver.quit()


def surfit_crawler_with_csv():
    driver = set_chrome_driver()

    posts = []
    initialize_jagged_list(list_name=posts, list_length=5)

    # 과정: 크롤링 -> items에 저장 -> csv 파일에 저장
    column = ["url", "title", "description", "category", "image"]
    for i, surfit_url in enumerate(surfit_url_list):
        one_cycle_of_crawling(driver, surfit_url, posts, i)
        items = append_data(
            urls=posts[0], titles=posts[1], descriptions=posts[2], category=posts[3], image=posts[4]
        )
        posts = [[], [], [], [], []]  # 리스트 초기화

        save_to_csv(
            file_name=f"csv_files/{category_list[i]}.csv", column=column, data=items
        )

    driver.quit()


def surfit_link_crawler_with_csv():
    driver = set_chrome_driver()

    for i, surfit_url in enumerate(surfit_url_list):
        urls = one_cycle_of_crawling_urls_by_category(
            driver=driver, url=surfit_url
        )
        save_to_csv(
            file_name=f"url_csv_files/{category_list[i]}.csv", column=[], data=urls
        )
        print("완료")

    driver.quit()


if __name__ == "__main__":
    surfit_crawler_with_csv()
