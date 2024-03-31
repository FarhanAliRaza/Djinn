import re
import subprocess
import sys

MODULE_REGEX = r"^[_a-zA-Z][_a-zA-Z0-9]+$"
module_name = "{{ cookiecutter.module_name }}"


def is_docker_installed() -> bool:
    try:
        subprocess.run(["docker", "--version"], capture_output=True, check=True)
        return True
    except Exception:
        return False


if __name__ == "__main__":
    if not is_docker_installed():
        print("ERROR: Docker is not installed.")
        sys.exit(1)

    if not re.match(MODULE_REGEX, module_name):
        print(f"ERROR: {module_name} is not a valid Python module name!")
        sys.exit(1)
