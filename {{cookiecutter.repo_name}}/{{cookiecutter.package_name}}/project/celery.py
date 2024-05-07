import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
# this is also used in manage.py
os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "{{cookiecutter.package_name}}.project.settings"
)

app = Celery("djinn")

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# We used CELERY_BROKER_URL in settings.py instead of:
# app.conf.broker_url = 'redis://localhost:6379/0'

# # We used CELERY_BEAT_SCHEDULER in settings.py instead of:
# app.conf.beat_scheduler = 'django_celery_beat.schedulers.DatabaseScheduler'


# app.conf.beat_schedule = {
#     "check_verifying_list": {
#         "task": "check_verifying_list",
#         "schedule": 10.0,
#     },
# }
