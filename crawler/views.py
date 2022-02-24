from rest_framework import viewsets
from rest_framework.decorators import action


class SurfitCrawlerView(viewsets.ViewSet):
    @action(detail=False)
    def categories(self, request):
        """
        surfit의 카테고리 목록을 반환한다.
        :param request:
        :return:
        """
        return
