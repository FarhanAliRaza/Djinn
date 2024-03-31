import os

os.environ["PYTEST_RUNNING"] = "true"

from {{cookiecutter.project_slug}}.common.tests.fixtures import *  # noqa: F401, F403, E402
from {{cookiecutter.project_slug}}.users.tests.fixtures import *  # noqa: F401, F403, E402
