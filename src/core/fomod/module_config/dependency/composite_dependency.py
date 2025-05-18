"""
Copyright (c) Cutleast
"""

from __future__ import annotations

from typing import Optional, override

from pydantic_xml import BaseXmlModel, attr, element
from PySide6.QtWidgets import QApplication

from core.utilities.localized_enum import LocalizedEnum

from .file_dependency import FileDependency
from .flag_dependency import FlagDependency
from .version_dependency import VersionDependency


class CompositeDependency(BaseXmlModel, tag="dependencies", search_mode="unordered"):
    """
    Model representing the compositeDependency tag of the ModuleConfig.xml.

    A dependency that is made up of one or more dependencies.
    """

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

        def get_display_name(self) -> str:
            """
            Returns:
                str: A display name generated from the dependencies.
            """

            return ", ".join(
                [dep.file for dep in self.file_dependencies]
                + [dep.flag for dep in self.flag_dependencies]
                + [
                    dep.version
                    for dep in [self.game_dependency, self.fomm_dependency]
                    if dep is not None
                ]
                + (
                    [self.dependencies.get_display_name()]
                    if self.dependencies is not None
                    else []
                )
            )

    dependencies: DependencyTypesGroup = element(
        tag="dependencies", default_factory=DependencyTypesGroup
    )
    """A list of dependencies."""

    class Operator(LocalizedEnum):
        """Enum for the relation of the contained dependencies."""

        And = "And"
        """
        Indicates all contained dependencies must be satisfied in order for this
        dependency to be satisfied.
        """

        Or = "Or"
        """
        Indicates at least one listed dependency must be satisfied in order for this
        dependency to be satisfied.
        """

        @override
        def get_localized_name(self) -> str:
            locs: dict[CompositeDependency.Operator, str] = {
                CompositeDependency.Operator.And: QApplication.translate(
                    "CompositeDependency", "And"
                ),
                CompositeDependency.Operator.Or: QApplication.translate(
                    "CompositeDependency", "Or"
                ),
            }

            return locs[self]

        @override
        def get_localized_description(self) -> str:
            locs: dict[CompositeDependency.Operator, str] = {
                CompositeDependency.Operator.And: QApplication.translate(
                    "CompositeDependency",
                    "All contained dependencies must be satisfied in order for this "
                    "dependency to be satisfied.",
                ),
                CompositeDependency.Operator.Or: QApplication.translate(
                    "CompositeDependency",
                    "At least one listed dependency must be satisfied in order for this "
                    "dependency to be satisfied.",
                ),
            }

            return locs[self]

    operator: Operator = attr(name="operator", default=Operator.And)
    """The relation of the contained dependencies."""

    def get_display_name(self) -> str:
        """
        Returns:
            str: A display name generated from the dependencies.
        """

        return self.dependencies.get_display_name()

    @override
    def __str__(self) -> str:
        return self.get_display_name()


CompositeDependency.model_rebuild()
CompositeDependency.DependencyTypesGroup.model_rebuild()
