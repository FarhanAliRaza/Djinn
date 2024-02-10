




from rest_framework.routers import DefaultRouter
from .views.task import TaskView


router = DefaultRouter()
router.register(r'tasks', TaskView, "task")

urlpatterns = router.urls
print(urlpatterns, "urlpatterns")
