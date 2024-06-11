from django.contrib import admin

# Register your models here.
from .models import OauthProvider

admin.site.register(OauthProvider)
