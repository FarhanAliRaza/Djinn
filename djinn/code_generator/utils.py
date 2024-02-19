import ast
from pathlib import Path
import os
from ..project.settings import BASE_DIR
from .consts import GenType


def pprintast(parsed_ast, indent=1):
    print(ast.dump(parsed_ast, indent=indent))


def get_app_file_path(filename: str, app_path: Path, type: str):
    if type == GenType.SERIALIZER:
        return app_path / f"serializers/{filename}.py"
    elif type == GenType.VIEW:
        return app_path / f"views/{filename}.py"
    elif type == GenType.URL:
        return app_path / "urls.py"


def write_or_append_to_file(filepath, data):

    if os.path.exists(filepath):
        print(f"appending to file {filepath}")
        with open(filepath, "a") as f:
            f.write(data)
    else:
        with open(filepath, "w") as f:
            f.write(data)


def danger_print(skk):
    print("\033[91m {}\033[00m".format(skk))


def space():
    print()
    print("--------------------------")
    print()
