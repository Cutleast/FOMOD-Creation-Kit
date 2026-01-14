"""
Copyright (c) Cutleast
"""

from typing import Optional

from PySide6.QtCore import QMimeData


class ClipboardMock:
    """
    Mocked clipboard for ui-related tests.

    Supports both text-based clipboard access and QMimeData-based access.

    Example usage in a pytest fixture:
    ```
    clipboard_mock = ClipboardMock()

    monkeypatch.setattr(
        "PySide6.QtWidgets.QApplication.clipboard",
        lambda: clipboard_mock,
    )

    yield clipboard_mock
    ```
    """

    __text: str = ""
    __mime_data: Optional[QMimeData] = None

    def setText(self, text: str) -> None:
        """
        Mimics `QClipboard.setText()`.
        """

        self.__text = text
        self.__mime_data = None

    def text(self) -> str:
        """
        Mimics `QClipboard.text()`.
        """

        return self.__text

    def setMimeData(self, mime_data: QMimeData) -> None:
        """
        Mimics `QClipboard.setMimeData()`.
        """

        self.__mime_data = mime_data
        self.__text = mime_data.text() if mime_data.hasText() else ""

    def mimeData(self) -> QMimeData | None:
        """
        Mimics `QClipboard.mimeData()`.
        """

        return self.__mime_data
