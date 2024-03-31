from enum import Enum
from pathlib import Path

from django.conf import settings

_BASEDIR = Path(__file__).resolve().parent
SOURCE = _BASEDIR / "source"
GENERATED = _BASEDIR / "generated"
BASEDIR = settings.BASE_DIR
PARENT_PACKAGE = (
    "{{cookiecutter.module_name}}"  # should be package name from cookiecutter
)
INSTALLED_APPS_SETTINGS_PATH = (
    BASEDIR / f"{PARENT_PACKAGE}" / "project" / "settings" / "base.py"
)


class GenType(Enum):
    VIEW = "views"
    SERIALIZER = "serializers"
    URL = "urls"


class Template(Enum):
    pass
