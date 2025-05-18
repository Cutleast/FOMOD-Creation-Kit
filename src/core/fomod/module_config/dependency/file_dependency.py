"""
Copyright (c) Cutleast
"""

from typing import override

from pydantic_xml import attr
from PySide6.QtWidgets import QApplication

from core.utilities.localized_enum import LocalizedEnum

from .dependency import Dependency


class FileDependency(Dependency, tag="fileDependency"):
    """
    Model representing the fileDependency tag of the ModuleConfig.xml.

    A mod upon which the type of a plugin depends.
    """

    file: str = attr(name="file")
    """The file of the mod upon which a plugin depends."""

    class State(LocalizedEnum):
        """
        Enum for the states of a mod file.
        """

        Missing = "Missing"
        """Indicates the mod file is not installed."""

        Inactive = "Inactive"
        """Indicates the mod file is installed, but not active."""

        Active = "Active"
        """Indicates the mod file is installed and active."""

        @override
        def get_localized_name(self) -> str:
            locs: dict[FileDependency.State, str] = {
                FileDependency.State.Missing: QApplication.translate(
                    "FileDependency", "Missing"
                ),
                FileDependency.State.Inactive: QApplication.translate(
                    "FileDependency", "Inactive"
                ),
                FileDependency.State.Active: QApplication.translate(
                    "FileDependency", "Active"
                ),
            }

            return locs[self]

        @override
        def get_localized_description(self) -> str:
            locs: dict[FileDependency.State, str] = {
                FileDependency.State.Missing: QApplication.translate(
                    "FileDependency", "The mod file is not installed."
                ),
                FileDependency.State.Inactive: QApplication.translate(
                    "FileDependency", "The mod file is installed, but is not active."
                ),
                FileDependency.State.Active: QApplication.translate(
                    "FileDependency", "The mod file is installed and active."
                ),
            }

            return locs[self]

    state: State = attr(name="state")
    """The state of the mod file."""

    TYPE: Dependency.Type = Dependency.Type.File
