"""
Copyright (c) Cutleast
"""

from __future__ import annotations

from typing import Optional

from pydantic_xml import BaseXmlModel, element

from .file_dependency import FileDependency
from .flag_dependency import FlagDependency
from .version_dependency import VersionDependency


class DependencyTypesGroup(BaseXmlModel, search_mode="unordered"):
    """
    Model representing a group of possible dependencies.
    """

    file_dependencies: list[FileDependency] = element(
        tag="fileDependency", default_factory=list
    )
    """List of file dependencies."""

    flag_dependencies: list[FlagDependency] = element(
        tag="flagDependency", default_factory=list
    )
    """List of flag dependencies."""

    game_dependency: Optional[VersionDependency] = element(
        tag="gameDependency", default=None
    )
    """Specifies a minimum required version of the installed game."""

    fomm_dependency: Optional[VersionDependency] = element(
        tag="fommDependency", default=None
    )
    """Specifies a minimum required version of FOMM."""

    dependencies: Optional[CompositeDependency] = element(
        tag="dependencies", default=None
    )
    """A list of mods and their states against which to match the user's installation."""


if __name__ == "__main__":
    from .composite_dependency import CompositeDependency
