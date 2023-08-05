"""This module contains everything related to the database."""
from __future__ import annotations

from pony import orm


# Can be removed with pytask v0.4.
try:
    from pytask import db
except ImportError:
    from _pytask.database_utils import db


class Environment(db.Entity):
    """Collects all information of the environment which should be checked."""

    name = orm.PrimaryKey(str)
    version = orm.Required(str)
    path = orm.Required(str)
