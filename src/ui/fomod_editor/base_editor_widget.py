"""
Copyright (c) Cutleast
"""

from abc import abstractmethod
from typing import Sequence

from pydantic_xml import BaseXmlModel
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QVBoxLayout, QWidget

from core.fomod.fomod import Fomod
from ui.widgets.smooth_scroll_area import SmoothScrollArea


class BaseEditorWidget[T: Fomod | BaseXmlModel | Sequence[BaseXmlModel]](
    SmoothScrollArea
):
    """
    Base class for all FOMOD editor widgets.
    """

    changed = Signal()
    """Signal emitted when the user makes a change to its edited item."""

    saved = Signal(object)
    """
    Signal emitted when the changes were saved.

    Args:
        T: The saved item
    """

    _item: T

    _vlayout: QVBoxLayout

    def __init__(self, item: T) -> None:
        super().__init__()

        self._item = item

        self._init_ui()

    def _init_ui(self) -> None:
        scroll_widget = QWidget()
        scroll_widget.setObjectName("transparent")
        scroll_widget.setContentsMargins(0, 0, 0, 0)
        self.setWidget(scroll_widget)

        self._vlayout = QVBoxLayout()
        self._vlayout.setContentsMargins(0, 0, 0, 0)
        self._vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll_widget.setLayout(self._vlayout)

    @classmethod
    @abstractmethod
    def get_display_name(cls) -> str:
        """
        Returns:
            str: Localized display name.
        """

    @abstractmethod
    def save(self) -> T:
        """
        Saves the user input to its item.

        Returns:
            T: The saved item
        """

    @abstractmethod
    def validate(self) -> None:
        """
        Validates the current item.

        Raises:
            ValidationError: If the item is invalid.
        """

    def get_item(self) -> T:
        """
        Returns:
            T: The current item
        """

        return self._item
