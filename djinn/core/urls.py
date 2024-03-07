from rest_framework.routers import DefaultRouter

from .views.blog import BlogViewSet

router = DefaultRouter()
router.register(r"blogs", BlogViewSet, "blogs_viewset")
urlpatterns = router.urls
