"""
Copyright (c) Cutleast
"""

from pathlib import Path
from typing import override

from PySide6.QtWidgets import QApplication

from core.utilities.exceptions import ExceptionBase


class ValidationError(ExceptionBase):
    """
    Exception when the FOMOD could not be saved due to validation errors (incomplete,
    missing or invalid fields).
    """


class SpecificValidationError(ValidationError):
    """
    ValidationError with a custom message.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)

    @override
    def _get_localized_message(self) -> str:
        return "{0}"


class EmptyError(ValidationError):
    """
    Exception when no field is filled.
    """

    @override
    def _get_localized_message(self) -> str:
        return QApplication.translate(
            "fomod_editor", "At least one item or field has to be specified!"
        )


class SpecificEmptyError(EmptyError):
    """
    EmptyError with a custom message.
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)

    @override
    def _get_localized_message(self) -> str:
        return "{0}"


class PathNotInFomodError(ValidationError):
    """
    Exception when the path of an image or a file is outside the FOMOD folder.
    """

    def __init__(self, invalid_path: Path, fomod_path: Path) -> None:
        super().__init__(str(invalid_path), str(fomod_path))

    @override
    def _get_localized_message(self) -> str:
        return QApplication.translate(
            "fomod_editor", "The path\n'{0}'\nis outside the FOMOD folder\n'{1}'!"
        )


class ImageTypeNotSupportedError(ValidationError):
    """
    Exception when the chosen image type is not supported by FOMOD installers.
    """

    def __init__(self, image_type: str) -> None:
        super().__init__(image_type)

    @override
    def _get_localized_message(self) -> str:
        return QApplication.translate(
            "fomod_editor",
            "The image type '{0}' is not supported by FOMOD installers!",
        )


class FileDoesNotExistError(ValidationError):
    """
    Exception when a file does not exist.
    """

    def __init__(self, file_path: Path) -> None:
        super().__init__(str(file_path))

    @override
    def _get_localized_message(self) -> str:
        return QApplication.translate(
            "fomod_editor", "The file\n'{0}'\ndoes not exist!"
        )


class FileNameIsMissingError(ValidationError):
    """
    Exception when the file name is missing.
    """

    @override
    def _get_localized_message(self) -> str:
        return QApplication.translate("fomod_editor", "The file name is missing!")


class NameIsMissingError(ValidationError):
    """
    Exception when a name is missing.
    """

    @override
    def _get_localized_message(self) -> str:
        return QApplication.translate("fomod_editor", "The name is missing!")


class ValueIsMissingError(ValidationError):
    """
    Exception when a value is missing.
    """

    @override
    def _get_localized_message(self) -> str:
        return QApplication.translate("fomod_editor", "The value is missing!")
