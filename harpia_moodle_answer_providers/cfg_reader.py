from importlib import util as import_util
from pathlib import Path
from typing import TypedDict, Protocol

ProviderArgs = TypedDict("ProviderArgs", {"name": str, "class": str})


class ConfigProtocol(Protocol):
    ANSWER_PROVIDERS: list[ProviderArgs]


def load_configuration(config_file: Path) -> ConfigProtocol:
    """Load a configuration from a file.

    Args:
        config_file: path to the configuration file

    Returns:
        the parsed configuration
    """
    if not config_file.exists():
        error = f"Configuration file {config_file} was not found"
        raise ValueError(error)
    spec = import_util.spec_from_file_location(config_file.name, config_file)
    if not spec or not spec.loader:
        error = "Could not load configuration file"
        raise ValueError(error)
    cfg = import_util.module_from_spec(spec)
    spec.loader.exec_module(cfg)
    return cfg
