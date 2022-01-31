from surfit_crawler.set_up_data import category_list


def parse_url_title_description(soup, tag_name, class_name, posts, index):
    items = soup.find_all(tag_name, class_name)

    for item in items:
        posts[0].append(item.find("div", "ct-title").contents[0].attrs['href'])  # url
        posts[1].append(item.find("div", "ct-title").text)  # title
        posts[2].append(item.find("div", "ct-text").text)  # description
        posts[3].append(category_list[index])  # category
