import random
from django.db import models
from django.contrib.auth.models import User


choices = (
    ("READY", "READY"),
    ("RUNNING", "RUNNING"),
    ("DONE", "DONE"),
)


class Task(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=choices)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
