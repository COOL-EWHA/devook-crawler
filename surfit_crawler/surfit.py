"""
Surfit Crawler

1. get post list page html from Surfit
2. parse url, title, description from html
3. insert url, title, description, category into mysql
"""
from surfit_crawler.set_up_data import surfit_url_list
from surfit_crawler.utils import (
    set_chrome_driver,
    append_data,
    initialize_jagged_list,
    one_cycle_of_crawling,
)
from surfit_crawler.utils_db import insert_into_database
from surfit_crawler.utils_csv import save_to_csv
from surfit_crawler.set_up_data import category_list


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
    initialize_jagged_list(list_name=posts, list_length=4)

    # 과정: 크롤링 -> items에 저장 -> csv 파일에 저장
    column = ["url", "title", "description", "category"]
    for i, surfit_url in enumerate(surfit_url_list):
        one_cycle_of_crawling(driver, surfit_url, posts, i)
        items = append_data(
            urls=posts[0], titles=posts[1], descriptions=posts[2], category=posts[3]
        )
        posts = [[], [], [], []]  # 리스트 초기화

        save_to_csv(
            file_name=f"csv_files/{category_list[i]}.csv", column=column, data=items
        )

    driver.quit()


if __name__ == "__main__":
    surfit_crawler_with_csv()
