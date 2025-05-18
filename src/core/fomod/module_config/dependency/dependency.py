"""
Copyright (c) Cutleast
"""

from typing import override

from pydantic_xml import BaseXmlModel
from PySide6.QtWidgets import QApplication

from core.utilities.localized_enum import LocalizedEnum


class Dependency(BaseXmlModel, search_mode="unordered"):
    """
    Base model for dependencies.
    """

    class Type(LocalizedEnum):
        """Enum for dependency types."""

        File = "File"
        """A mod upon which the type of a plugin depends."""

        Flag = "Flag"
        """A condition flag upon which the type of a plugin depends."""

        Version = "Version"
        """A required minimum version of an item."""

        @override
        def get_localized_name(self) -> str:
            locs: dict[Dependency.Type, str] = {
                Dependency.Type.File: QApplication.translate("Dependency", "File"),
                Dependency.Type.Flag: QApplication.translate("Dependency", "Flag"),
                Dependency.Type.Version: QApplication.translate(
                    "Dependency", "Version"
                ),
            }

            return locs[self]

        @override
        def get_localized_description(self) -> str:
            locs: dict[Dependency.Type, str] = {
                Dependency.Type.File: QApplication.translate(
                    "Dependency",
                    "A mod upon which the type of a plugin depends.",
                ),
                Dependency.Type.Flag: QApplication.translate(
                    "Dependency",
                    "A condition flag upon which the type of a plugin depends.",
                ),
                Dependency.Type.Version: QApplication.translate(
                    "Dependency",
                    "A required minimum version of an item.",
                ),
            }

            return locs[self]
