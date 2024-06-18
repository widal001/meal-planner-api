"""Manage configuration settings using dynaconf."""

from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="MEAL_PLANNER",
    settings_files=["settings.toml", ".secrets.toml"],
    environments=True,
)
