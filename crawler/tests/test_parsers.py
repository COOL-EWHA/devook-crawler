from unittest import TestCase

from crawler.utils.utils import parse_url_title_description
from crawler.utils.utils import (
    set_chrome_driver,
    loads_a_web_page_in_the_current_session,
    web_page_scroll,
    set_beautifulsoup,
    initialize_jagged_list,
)


class ParsersTestCase(TestCase):
    posts = []

    @classmethod
    def setUpClass(cls) -> None:
        initialize_jagged_list(list_name=cls.posts, list_length=4)

    def test_parse_url_title_description(self):
        """
        성공 : 파싱한 데이터의 개수와 리스트에 저장된 개수가 동일한 경우
        """
        # given
        url = "https://www.surfit.io/explore/develop/ios"
        index = 13
        driver, soup = self.set_chrome_driver_and_beautifulsoup(url)
        expected = len(soup.find_all("div", "ct-item base"))
        # when
        parse_url_title_description(
            soup=soup,
            tag_name="div",
            class_name="ct-item base",
            posts=self.posts,
            index=index,
        )
        result = len(self.posts[0])
        print(self.posts)
        driver.quit()
        # then
        self.assertEqual(expected, result)

    @staticmethod
    def set_chrome_driver_and_beautifulsoup(url):
        driver = set_chrome_driver()
        loads_a_web_page_in_the_current_session(driver=driver, url=url)
        web_page_scroll(driver=driver)
        soup = set_beautifulsoup(driver=driver)
        return driver, soup
