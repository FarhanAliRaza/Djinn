import shutil
from pathlib import Path

module_name = "{{ cookiecutter.package_name }}"


def remove_dotgithub_folder():
    shutil.rmtree(".github")


def remove_celery_files():
    celery_file = Path("{{cookiecutter.package_name}}/project/celery.py")
    celery_settings_file = Path(
        "{{cookiecutter.package_name}}/project/settings/celery.py"
    )
    celery_file.unlink()
    celery_settings_file.unlink()


if __name__ == "__main__":
    if not {{cookiecutter.use_github_actions}}:
        remove_dotgithub_folder()
    if not {{cookiecutter.use_celery}}:
        remove_celery_files()
