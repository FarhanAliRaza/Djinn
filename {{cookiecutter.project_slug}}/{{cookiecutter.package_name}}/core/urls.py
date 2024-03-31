from rest_framework.routers import DefaultRouter

from .views.blog import BlogViewSet

router = DefaultRouter(trailing_slash=False)
router.register(r"blogs", BlogViewSet, "blogs_viewset")
urlpatterns = router.urls
