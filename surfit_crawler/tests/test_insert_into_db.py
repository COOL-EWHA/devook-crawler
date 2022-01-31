from unittest import TestCase

from surfit_crawler.parsers import parse_url_title_description
from surfit_crawler.utils import set_chrome_driver, \
    initialize_jagged_list, \
    convert_driver_to_beautifulsoup, \
    append_data, insert_into_database, connect_db, disconnect_db


class InsertIntoDBTestCase(TestCase):
    posts = []

    @classmethod
    def setUpClass(cls) -> None:
        initialize_jagged_list(list_name=cls.posts, list_length=4)

        cls.driver = set_chrome_driver()
        cls.conn = connect_db("root", "cool", "127.0.0.1", "test_db")

    def test_insert_into_db(self):
        """
        성공 : 파싱한 데이터의 개수와 데이터베이스에 저장된 개수가 동일한 경우
        """
        url = "https://www.surfit.io/explore/develop/ios"
        index = 13

        soup = convert_driver_to_beautifulsoup(self.driver, url)
        self.driver.quit()

        expected = len(soup.find_all("div", "ct-item base"))

        parse_url_title_description(soup=soup, tag_name="div", class_name="ct-item base", posts=self.posts, index=index)
        items = append_data(urls=self.posts[0], titles=self.posts[1], descriptions=self.posts[2],
                            category=self.posts[3])
        insert_into_database(items=items, user="root", passwd="cool", host="127.0.0.1", db="test_db")

        sql = "SELECT * FROM post;"
        result = self.conn.cursor().execute(sql)
        disconnect_db(self.conn)

        self.assertEqual(expected, result)
