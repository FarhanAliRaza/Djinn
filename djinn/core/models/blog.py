from django.db import models


class StatusChoice(models.TextChoices):
    published = "published"
    draft = "draft"


class Blog(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField()
    status = models.CharField(max_length=100, choices=StatusChoice.choices, default=StatusChoice.published)
