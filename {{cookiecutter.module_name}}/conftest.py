import os

os.environ["PYTEST_RUNNING"] = "true"

from djinn.common.tests.fixtures import *  # noqa: F401, F403, E402
from djinn.users.tests.fixtures import *  # noqa: F401, F403, E402
