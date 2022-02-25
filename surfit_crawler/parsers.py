from surfit_crawler.set_up_data import category_list


def parse_url_title_description(soup, tag_name, class_name, posts, index):
    items = soup.find_all(tag_name, class_name)

    for item in items:
        posts[0].append(item.find("div", "ct-title").contents[0].attrs["href"])  # url
        posts[1].append(item.find("div", "ct-title").text)  # title
        posts[2].append(item.find("div", "ct-text").text)  # description
        posts[3].append(category_list[index])  # category


def parse_categories(
        soup, find_tag_name, find_class_name, find_all_tag_name, find_all_class_name
):
    """
    :param soup: Beautiful()의 object
    :param find_tag_name:
    :param find_class_name:
    :param find_all_tag_name:
    :param find_all_class_name:
    :return: 카테고리 목록
    """
    categories = []

    categories_html_a = soup.find(find_tag_name, find_class_name)
    if categories_html_a is None:  # 예외 처리
        return categories
    categories_html_b = categories_html_a.find_all(
        find_all_tag_name, find_all_class_name
    )

    for category in categories_html_b:
        categories.append(category.text)
    return categories


def parse_urls(soup, tag_name, class_name):
    items = soup.find_all(tag_name, class_name)

    urls = []
    for item in items:
        urls.append(item.find("div", "ct-title").contents[0].attrs["href"])  # url
    return urls
