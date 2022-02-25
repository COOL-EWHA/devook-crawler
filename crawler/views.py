from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from surfit_crawler.utils import (
    get_surfit_dev_categories,
    set_chrome_driver,
    get_urls_by_all_category,
    one_cycle_of_crawling_urls_by_category,
    get_surfit_url_by_category_dict,
)
from surfit_crawler.set_up_data import category_list


class SurfitCrawlerViewSet(viewsets.ViewSet):
    surfit_url_by_category_dict = get_surfit_url_by_category_dict()

    @action(detail=False)
    def categories(self, request):
        """
        surfit의 카테고리 목록을 반환한다.
        :param request:
        :return:
        """
        driver = set_chrome_driver()
        url = "https://www.surfit.io/explore/develop"
        categories = get_surfit_dev_categories(driver=driver, url=url)
        driver.quit()
        return Response(data={"categories": categories}, status=status.HTTP_200_OK)

    def list(self, request):
        """
        surfit의 개발 카테고리별 링크의 목록을 반환한다.
        :param request:
        :return:
        """
        # /surfit?category={param}
        if request.query_params:
            try:
                category = request.query_params["category"]
                url = self.surfit_url_by_category_dict[category]  # 해당 카테고리의 url
                driver = set_chrome_driver()
            except KeyError:
                return Response(
                    data={"올바르지 않은 query param 입니다."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            urls = one_cycle_of_crawling_urls_by_category(driver=driver, url=url)
            driver.quit()
            return Response(data={category: urls}, status=status.HTTP_200_OK)

        # /surfit
        driver = set_chrome_driver()

        urls_by_all_category = []
        get_urls_by_all_category(
            driver=driver, urls_by_all_category_list=urls_by_all_category
        )
        driver.quit()

        data = {}
        for i, category in enumerate(category_list):
            data[category] = urls_by_all_category[i]

        return Response(data=data, status=status.HTTP_200_OK)
