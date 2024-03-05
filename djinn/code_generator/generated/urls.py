from rest_framework.routers import DefaultRouter
from .views.blog import BlogViewSet


router = DefaultRouter()
router.register(r"blogs", BlogViewSet, "blog_view")
urlpatterns = router.urls
