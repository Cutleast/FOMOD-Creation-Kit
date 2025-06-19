"""
Copyright (c) Cutleast
"""

from pathlib import Path
from typing import override

from PySide6.QtWidgets import QApplication

from core.utilities.exceptions import ExceptionBase


class NotAFomodError(ExceptionBase):
    """
    Exception when a specified path does not point to a FOMOD installer.
    """

    def __init__(self, path: Path) -> None:
        super().__init__(path)

    @override
    def _get_localized_message(self) -> str:
        return QApplication.translate(
            "exceptions", "The path ('{0}') does not point to a FOMOD installer!"
        )


class XmlValidationError(ExceptionBase):
    """
    Exception when the FOMOD could not be saved due to XML validation errors.
    """

    def __init__(self, file_name: str) -> None:
        super().__init__(file_name)

    @override
    def _get_localized_message(self) -> str:
        return QApplication.translate(
            "exceptions",
            "Failed to save the FOMOD installer! Could not validate '{0}'.",
        )
