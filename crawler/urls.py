from rest_framework import routers

from crawler.views import SurfitCrawlerViewSet

app_name = "crawler"

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"surfit", SurfitCrawlerViewSet, basename="surfit")

urlpatterns = router.urls
