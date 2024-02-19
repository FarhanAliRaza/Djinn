from pathlib import Path
from enum import Enum


_BASEDIR = Path(__file__).resolve().parent
SOURCE = _BASEDIR / "source"
GENERATED = _BASEDIR / "generated"


class GenType(Enum):
    VIEW = "views"
    SERIALIZER = "serializers"
    URL = "urls"
