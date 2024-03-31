from {{cookiecutter.module_name}}.common.utils.collections import deep_update
from {{cookiecutter.module_name}}.common.utils.settings import get_settings_from_environment

deep_update(globals(), get_settings_from_environment(ENVVAR_SETTINGS_PREFIX))  # type: ignore # noqa: F821
