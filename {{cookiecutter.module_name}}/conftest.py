import os

os.environ["PYTEST_RUNNING"] = "true"

from {{cookiecutter.module_name}}.common.tests.fixtures import *  # noqa: F401, F403, E402
from {{cookiecutter.module_name}}.users.tests.fixtures import *  # noqa: F401, F403, E402
