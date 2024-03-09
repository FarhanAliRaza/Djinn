from django.contrib.auth.models import AbstractUser
from django.db import models

from ..managers.user import UserManager


class User(AbstractUser):
    test = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    objects = UserManager()
