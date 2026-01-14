"""
Copyright (c) Cutleast
"""

from typing import cast

from pydantic import BaseModel
from PySide6.QtCore import QMimeData
from PySide6.QtWidgets import QApplication


class Clipboard:
    """
    Utility class for copying and pasting Pydantic objects to/from the clipboard.
    """

    MIME_TYPE: str = "application/x-cutleast-fomod-creation-kit+json"
    """The MIME type used for storing the objects in the clipboard."""

    class ClipboardPayload(BaseModel):
        """Payload that is stored in the clipboard."""

        type: str
        """The qualified name of the object's class."""

        data: str
        """The JSON string representation of the object."""

    @classmethod
    def copy(cls, obj: BaseModel) -> None:
        """
        Serializes the object to a JSON string and copies it to the clipboard.

        Args:
            obj (BaseModel): The object to copy to the clipboard.
        """

        payload = cls.ClipboardPayload(
            type=obj.__class__.__qualname__, data=obj.model_dump_json()
        )
        mime_data = QMimeData()
        mime_data.setData(cls.MIME_TYPE, payload.model_dump_json().encode())
        QApplication.clipboard().setMimeData(mime_data)

    @classmethod
    def contains_valid_obj(cls, obj_cls: type[BaseModel]) -> bool:
        """
        Checks if the clipboard contains an object of a specified type.

        Args:
            obj_cls (type[BaseModel]): The class of the object to check.

        Returns:
            bool: Whether the clipboard contains an object of the specified type.
        """

        mime_data: QMimeData = QApplication.clipboard().mimeData()

        if not mime_data.hasFormat(cls.MIME_TYPE):
            return False

        data: bytes = cast(bytes, mime_data.data(cls.MIME_TYPE).data())
        payload = cls.ClipboardPayload.model_validate_json(data)

        if payload.type != obj_cls.__qualname__:
            return False

        return True

    @classmethod
    def paste[T: BaseModel](cls, obj_cls: type[T]) -> T:
        """
        Attempts to paste an object of a specified type from the clipboard.

        Raises:
            ValueError:
                If the clipboard does not contain a valid object of the specified type.

        Returns:
            T: The pasted object.
        """

        mime_data: QMimeData = QApplication.clipboard().mimeData()

        if not mime_data.hasFormat(cls.MIME_TYPE):
            raise ValueError(
                "Clipboard does not contain a valid object of type "
                f"'{obj_cls.__qualname__}'."
            )

        data: bytes = cast(bytes, mime_data.data(cls.MIME_TYPE).data())
        payload = cls.ClipboardPayload.model_validate_json(data)

        if payload.type != obj_cls.__qualname__:
            raise ValueError(
                "Clipboard does not contain a valid object of type "
                f"'{obj_cls.__qualname__}'."
            )

        return obj_cls.model_validate_json(payload.data)
