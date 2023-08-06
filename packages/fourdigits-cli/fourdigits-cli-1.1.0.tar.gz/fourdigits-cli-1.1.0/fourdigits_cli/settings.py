import logging
import os
from dataclasses import dataclass, field

import tomli

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class EnvironmentConfig:
    name: str = ""


@dataclass(frozen=True)
class Config:
    docker_repo: str = ""
    docker_image_user: str = "fourdigits"
    environments: dict[str, EnvironmentConfig] = field(default_factory=dict)


def load_config(py_project_paths: list):
    config = {}
    for path in py_project_paths:
        if os.path.exists(path):
            try:
                with open(path, "rb") as f:
                    config = tomli.load(f).get("tool", {}).get("fourdigits", {})
            except tomli.TOMLDecodeError as e:
                logger.warning(f"Could not load pyproject.toml file: {e}")
                config = {}

    kwargs = {
        key: value for key, value in config.items() if key in Config.__annotations__
    }

    # Get environments
    kwargs["environments"] = {}
    for group, group_config in config.get("envs", {}).items():
        kwargs["environments"][group] = EnvironmentConfig(
            **{
                key: value
                for key, value in group_config.items()
                if key in EnvironmentConfig.__annotations__
            }
        )

    return Config(**kwargs)


DEFAULT_CONFIG = load_config(
    [
        os.path.join(os.getcwd(), "pyproject.toml"),
        os.path.join(os.getcwd(), "src", "pyproject.toml"),
    ]
)
