from .views.blog import BlogViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"blogs", BlogViewSet, "blogs_viewset")
urlpatterns = router.urls
