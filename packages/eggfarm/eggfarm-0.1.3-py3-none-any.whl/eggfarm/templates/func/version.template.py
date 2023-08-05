import importlib.metadata

package_metadada = importlib.metadata.metadata("{{ func_name }}")
# info from pyproject.toml's `version` and `description`
VERSION = package_metadada.get("Version")


def {{ func_name }}_version():
    return VERSION
