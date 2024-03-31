import os
from pathlib import Path
from typing import List

import django
from django.apps import apps
from django.db import models

os.environ["DJANGO_SETTINGS_MODULE"] = "{{cookiecutter.module_name}}.project.settings"
django.setup()

read_only_models = [
    "User",
    "Group",
    "Permission",
    "ContentType",
    "Session",
    "Site",
    "LogEntry",
]
REALATION_FIELDS_CLASSES = (
    models.ForeignKey,
    models.ManyToManyField,
    models.OneToOneField,
)


class Generator:
    def __init__(self, app_name, model_name):
        self.app_name: str = app_name
        self.model_name: str = model_name
        self.app_path: Path = Path(apps.get_app_config(self.app_name).path)
        self.relation_fields: List = []
        self.read_only_fields: List = []
        self.fields: List = []
        self.str_fields: List[str] = []
        self.get_model()
        self.get_fields()

    def get_model(self) -> None:
        self.model = apps.get_model(self.app_name, self.model_name)

    def get_fields(self) -> tuple:
        return self.model._meta.fields

    def get_model_name(self, model=None) -> str:
        if model is None:
            return self.model._meta.label.split(".")[1]
        return model._meta.label.split(".")[1]

    def parse(self):
        for field in self.get_fields():
            if field.__class__ in REALATION_FIELDS_CLASSES:
                if self.get_model_name(field.related_model) in read_only_models:
                    self.read_only_fields.append(field)
                self.relation_fields.append(field)
            else:
                self.fields.append(field)


if __name__ == "__main__":
    pass
