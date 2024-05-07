from cookiecutter.main import cookiecutter
from cookiecutter.replay import dump
from cookiecutter.generate import generate_context
from pathlib import Path
import shutil

BASE_DIR = Path(__file__).parent.parent


def create_project():
    cookiecutter(str(BASE_DIR))


def remove_generated():
    shutil.rmtree("djinn")


if __name__ == "__main__":
    create_project()
