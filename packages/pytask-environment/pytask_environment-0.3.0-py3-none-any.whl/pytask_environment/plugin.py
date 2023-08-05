"""Entry-point for the plugin."""
from __future__ import annotations

from pluggy import PluginManager
from pytask import hookimpl
from pytask_environment import config
from pytask_environment import database
from pytask_environment import logging


@hookimpl
def pytask_add_hooks(pm: PluginManager) -> None:
    """Register some plugins."""
    pm.register(logging)
    pm.register(config)
    pm.register(database)
