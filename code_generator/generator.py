import django
import os
from django.apps import apps
import sys
from django.db import models
from parser import Parser
import ast
from utils import pprintast
from serializer import GenerateSerializer

sys.path.append("..")
os.environ["DJANGO_SETTINGS_MODULE"] = "project.settings"
django.setup()

from django.
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
        self.relation_fields: list = []
        self.read_only_fields:list = []
        self.fields: list = []
        self.get_model()
        self.get_fields()

    def get_model(self) -> None:
        self.model = apps.get_model(self.app_name, self.model_name)

    def get_fields(self) -> tuple:
        return self.model._meta.fields

    def get_model_name(self,model=None)->str:
        if model is None:
            return self.model._meta.label.split(".")[1]
        return model._meta.label.split(".")[1]

    def get_label(self) -> str:
        return self.model._meta.label

    # TODO: create serializers recursively but issue is that what we are gonna do about views

    def parse(self):
        for field in self.get_fields():
            if field.__class__ in REALATION_FIELDS_CLASSES:
                if self.get_model_name(field.related_model) in read_only_models:
                    self.read_only_fields.append(field)
                self.relation_fields.append(field)

            else:
                self.fields.append(field)

    def create_serializer(
        self,
    ):
        pass

    def create_views(
        self,
    ):
        pass


def main():
    # app specific
    gen = Generator("core", "Task")
    gen.parse()
    g = GenerateSerializer(gen)
    g.generate_serializer()


if __name__ == "__main__":
    main()
