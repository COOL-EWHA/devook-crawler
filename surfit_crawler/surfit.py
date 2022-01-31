"""
Surfit Crawler

1. get post list page html from Surfit
2. parse url, title, description from html
3. insert url, title, description, category into mysql
"""
from surfit_crawler.set_up_data import surfit_url_list
from surfit_crawler.utils import set_chrome_driver, \
    append_data, \
    insert_into_database, \
    initialize_jagged_list, \
    one_cycle_of_crawling


def surfit_crawler():
    driver = set_chrome_driver()

    posts = []
    initialize_jagged_list(list_name=posts, list_length=4)

    for i, surfit_url in enumerate(surfit_url_list):
        one_cycle_of_crawling(driver, surfit_url, posts, i)

    items = append_data(urls=posts[0], titles=posts[1], descriptions=posts[2], category=posts[3])
    insert_into_database(items=items, user="root", passwd="cool", host="127.0.0.1", db="devook_db")

    driver.quit()


if __name__ == '__main__':
    surfit_crawler()
