from crawler.utils.utils import *
from crawler.utils.utils_csv import *
from crawler.tistory.set_up_data import *
from crawler.tistory.utils import *


def tistory_crawler_with_csv():
    driver = set_chrome_driver()

    posts = []
    initialize_jagged_list(list_name=posts, list_length=1)

    # 과정: 크롤링 -> items에 저장 -> csv 파일에 저장
    column = ["title"]
    for i, url in enumerate(tistory_url_list):
        one_cycle_of_crawling_tistory(driver, url, posts, i)
        items = append_data_tistory(posts[0])
        posts = [[]]  # 리스트 초기화

        save_to_csv(
            file_name=f"csv_files/{category_list[i]}.csv", column=column, data=items
        )

    driver.quit()


if __name__ == "__main__":
    tistory_crawler_with_csv()
