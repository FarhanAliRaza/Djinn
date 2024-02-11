import random
from django.db import models
from django.contrib.auth.models import User
from common.utils import get_filename_ext


def upload_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    final_filename = "{new_filename}{ext}".format(new_filename=new_filename, ext=ext)
    return "files/{final_filename}".format(
        new_filename=new_filename, final_filename=final_filename
    )


statuses =  (
    ('ready', 'Ready'),
    ('verifying', 'Verifying'),
    ('done', 'Done'),
)


class Task(models.Model):

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=statuses, default='ready')
    file = models.FileField(upload_to='uploads/')
    slug = models.SlugField(max_length=100, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)



