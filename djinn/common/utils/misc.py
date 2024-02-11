import yaml


def yaml_coerce(value):
    # convert dict strings dict to python dicts
    if isinstance(value, str):
        return yaml.load(f"dummy: {value}", Loader=yaml.SafeLoader)["dummy"]

    return value
