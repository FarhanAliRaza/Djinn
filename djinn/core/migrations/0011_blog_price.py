# Generated by Django 5.0.2 on 2024-03-06 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_blog_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='price',
            field=models.FloatField(default=0.0),
        ),
    ]
