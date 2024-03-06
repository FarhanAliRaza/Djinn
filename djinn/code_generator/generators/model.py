from pathlib import Path
from django.db import models
from django.apps import apps

field_map = {
    "string": models.CharField,
    "text": models.TextField,
    "choice": models.CharField,
    "int": models.IntegerField,
    "float": models.FloatField,
}


class ModelGenerator:

    def __init__(self, app_name, model_name, generate=False) -> None:
        self.app_name = app_name
        self.model_name = model_name
        self.app_path: Path = Path(apps.get_app_config(self.app_name).path)

    def create_model(self):
        pass

    def add_to_admin(self):
        pass
