from rest_framework.routers import DefaultRouter
from .views.model import View


router = DefaultRouter()
router.register(r"models", View, "model")
urlpatterns = router.urls
