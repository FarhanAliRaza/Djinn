from django.db import models


class StatusChoice(models.TextChoices):
    draft = 0
    published = 1


class Blog(models.Model):
    title = models.CharField(max_length=255)
    status = models.CharField(
        max_length=100, choices=StatusChoice.choices, default=StatusChoice.draft
    )
    views = models.IntegerField(default=0)
