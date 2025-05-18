"""
Copyright (c) Cutleast
"""

from pydantic_xml import attr

from .dependency import Dependency


class VersionDependency(Dependency, tag="versionDependency"):
    """
    Model representing a required minimum version of an item.
    """

    version: str = attr(name="version")
    """The required minimum version of the item."""

    TYPE: Dependency.Type = Dependency.Type.Version
