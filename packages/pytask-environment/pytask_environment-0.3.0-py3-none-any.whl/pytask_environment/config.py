"""This module contains everything related to the configuration."""
from __future__ import annotations

from typing import Any

import click
from pytask import hookimpl


@hookimpl
def pytask_extend_command_line_interface(cli: click.Group) -> None:
    """Extend the cli."""
    cli.commands["build"].params.append(
        click.Option(
            ["--update-environment"],
            is_flag=True,
            default=False,
            help="Update the information on the environment stored in the database.",
        )
    )


@hookimpl
def pytask_parse_config(config: dict[str, Any]) -> None:
    """Parse the configuration."""
    config["check_python_version"] = config.get("check_python_version", True)
    config["check_environment"] = config.get("check_environment", True)
    config["update_environment"] = config.get("update_environment", False)
