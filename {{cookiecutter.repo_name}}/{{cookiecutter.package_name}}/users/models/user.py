from django.contrib.auth.models import AbstractUser
from django.db import models

from ..managers.user import UserManager


class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    is_social = models.BooleanField(default=False)
    USERNAME_FIELD = "email"
    name = models.CharField(null=True, blank=True)
    REQUIRED_FIELDS = []
    objects = UserManager()
    username = None  # type: ignore[assignment]
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)