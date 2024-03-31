from django.db import models


class ProviderChoice(models.TextChoices):
    GOOGLE = "GOOGLE"


class OauthProvider(models.Model):
    client_id = models.CharField(max_length=255)
    secret = models.CharField(max_length=255)
    provider = models.CharField(
        max_length=100, choices=ProviderChoice.choices, default=ProviderChoice.GOOGLE
    )

    def __str__(self) -> str:
        return self.provider
