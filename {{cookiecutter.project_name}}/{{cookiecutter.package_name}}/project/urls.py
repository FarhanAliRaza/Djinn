from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

API_PREFIX = "api/"

urlpatterns = [
    path("admin/", admin.site.urls),
    path(API_PREFIX, include("{{cookiecutter.package_name}}.users.urls")),
    path(API_PREFIX, include("{{cookiecutter.package_name}}.authentication.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
