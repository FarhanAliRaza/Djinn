from rest_framework.routers import DefaultRouter
from .views.task import TaskViewSet


router = DefaultRouter()
router.register(r"tasks", TaskViewSet, "task_view")
urlpatterns = router.urls
