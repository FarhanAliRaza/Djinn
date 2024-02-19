# Generated by Django 5.0 on 2024-02-02 23:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("ready", "Ready"),
                            ("verifying", "Verifying"),
                            ("done", "Done"),
                        ],
                        default="ready",
                        max_length=100,
                    ),
                ),
                ("verified_emails", models.PositiveIntegerField(default=0)),
                ("download_code", models.CharField(blank=True, max_length=100)),
                ("is_premium", models.BooleanField(default=False)),
                ("file", models.FileField(upload_to="uploads/")),
                ("slug", models.SlugField(blank=True, max_length=100)),
                ("v_emails", models.PositiveIntegerField(default=0)),
                ("i_emails", models.PositiveIntegerField(default=0)),
                ("c_emails", models.PositiveIntegerField(default=0)),
                ("u_emails", models.PositiveIntegerField(default=0)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
