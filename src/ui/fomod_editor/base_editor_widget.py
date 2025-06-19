"""
Copyright (c) Cutleast
"""

from abc import abstractmethod
from pathlib import Path
from typing import Optional, Sequence

from pydantic_xml import BaseXmlModel
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

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
    _fomod_path: Optional[Path]

    __show_title: bool
    __show_description: bool

    _vlayout: QVBoxLayout

    def __init__(
        self,
        item: T,
        fomod_path: Optional[Path],
        show_title: bool = False,
        show_description: bool = True,
    ) -> None:
        """
        Args:
            item (T): Edited item
            fomod_path (Optional[Path]):
                Path to the FOMOD, if any. Used for validation and display of images.
                Defaults to None.
            show_title (bool, optional):
                Whether to show the title at the top. Defaults to False.
            show_description (bool, optional):
                Whether to show the description at the top, if any. Defaults to True.
        """

        super().__init__()

        self._item = item
        self._fomod_path = fomod_path

        self.__show_title = show_title
        self.__show_description = show_description

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

        if self.__show_title:
            title_label = QLabel(self.get_title().strip() or self.get_display_name())
            title_label.setObjectName("h2")
            self._vlayout.addWidget(title_label)

        if self.__show_description and self.get_description().strip():
            help_label = QLabel(self.get_description())
            help_label.setWordWrap(True)
            self._vlayout.addWidget(help_label)

    @classmethod
    @abstractmethod
    def get_display_name(cls) -> str:
        """
        Returns:
            str: Localized display name.
        """

    @classmethod
    def get_title(cls) -> str:
        """
        Returns:
            str: Localized title. If empty, the display name will be used, instead.
        """

        return ""

    @classmethod
    def get_description(cls) -> str:
        """
        Returns:
            str: Localized description.
        """

        return ""

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
