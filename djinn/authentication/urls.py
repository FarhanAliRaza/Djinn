from django.urls import path

from .views.google import GoogleOauth
from .views.login import LoginView

urlpatterns = [
    path("login", LoginView.as_view()),
    path("oauth", GoogleOauth.as_view(), name="social_redirect"),
]
