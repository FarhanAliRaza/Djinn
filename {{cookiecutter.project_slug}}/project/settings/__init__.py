import os
from pathlib import Path

from djinn.common.utils.pytest import is_pytest_running
from split_settings.tools import include, optional

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
ENVVAR_SETTINGS_PREFIX = "DJINN_SETTING_"
LOCAL_SETTINGS_PATH = os.getenv(f"{ENVVAR_SETTINGS_PREFIX}LOCAL_SETTINGS_PATH")

if not LOCAL_SETTINGS_PATH:
    LOCAL_SETTINGS_PATH = (
        f'local/settings{".unittests" if is_pytest_running() else ".dev"}.py'
        # "local/settings.dev.py"
    )

if not os.path.isabs(LOCAL_SETTINGS_PATH):
    LOCAL_SETTINGS_PATH = str(BASE_DIR / LOCAL_SETTINGS_PATH)

include(
    "base.py",
    "custom.py",
    "logging.py",
    "drf.py",
    optional(LOCAL_SETTINGS_PATH),
    "jwt.py",  # because it requires SECRET_KEY
    "envvars.py",
    "docker.py",
)


if not is_pytest_running():
    assert SECRET_KEY is not NotImplemented  # noqa: F821, F403
