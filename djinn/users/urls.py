from django.urls import path
from rest_framework.routers import SimpleRouter

from .views.login import LoginView
from .views.user import UserViewSet

router = SimpleRouter(trailing_slash=False)
router.register("users", UserViewSet)
urlpatterns = [
    path("login", LoginView.as_view()),
] + router.urls
