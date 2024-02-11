import random
from django.db import models
from django.contrib.auth.models import User


statuses = (
    ("ready", "Ready"),
    ("verifying", "Verifying"),
    ("done", "Done"),
)


class Model(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=statuses, default="ready")
    is_premium = models.BooleanField(default=False)
    file = models.FileField(upload_to="uploads/")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
