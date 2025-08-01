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


class CompositeDependency(BaseXmlModel, search_mode="unordered"):
    """
    Model representing the compositeDependency tag of the ModuleConfig.xml.

    A dependency that is made up of one or more dependencies.
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

    dependencies: list[CompositeDependency] = element(
        tag="dependencies", default_factory=list
    )
    """A list of mods and their states against which to match the user's installation."""

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

        if self.is_empty():
            return (
                "<"
                + QApplication.translate("CompositeDependency", "empty dependency")
                + ">"
            )

        deps: list[str] = []

        deps.extend(
            [
                f"{dep.file} ({dep.state.get_localized_name()})"
                for dep in self.file_dependencies
            ]
        )
        deps.extend([dep.get_display_name() for dep in self.flag_dependencies])

        if self.game_dependency is not None:
            deps.append(
                QApplication.translate("CompositeDependency", "Game Version")
                + "="
                + self.game_dependency.version
            )
        if self.fomm_dependency is not None:
            deps.append(
                QApplication.translate("CompositeDependency", "FOMM Version")
                + "="
                + self.fomm_dependency.version
            )

        for dep in self.dependencies:
            if len(dep) > 1:
                deps.append("(" + dep.get_display_name() + ")")
            else:
                deps.append(dep.get_display_name())

        if len(deps) > 1:
            text = (
                ", ".join(deps[:-1])
                + " "
                + self.operator.get_localized_name().lower()
                + " "
                + deps[-1]
            )
        else:
            text = deps[0]

        return text

    @override
    def __str__(self) -> str:
        return self.get_display_name()

    def __len__(self) -> int:
        size: int = 0
        size += len(self.file_dependencies)
        size += len(self.flag_dependencies)
        size += 1 if self.game_dependency is not None else 0
        size += 1 if self.fomm_dependency is not None else 0
        size += len(self.dependencies)

        return size

    def is_empty(self) -> bool:
        """
        Returns:
            bool: `True` if this dependency is empty, `False` otherwise.
        """

        return not any(
            [
                self.file_dependencies,
                self.flag_dependencies,
                self.game_dependency,
                self.fomm_dependency,
                self.dependencies,
            ]
        )


CompositeDependency.model_rebuild()
