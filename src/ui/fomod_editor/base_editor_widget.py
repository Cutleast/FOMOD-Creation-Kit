"""
Copyright (c) Cutleast
"""

from abc import abstractmethod
from pathlib import Path
from typing import Callable, Optional, Sequence

from pydantic_xml import BaseXmlModel
from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from core.fomod.fomod import Fomod
from ui.widgets.smooth_scroll_area import SmoothScrollArea

type FlagNamesSupplier = Callable[[], list[str]]
"""
A function that returns an up-to-date list of all flag names from the current FOMOD.
"""


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
    _flag_names_supplier: FlagNamesSupplier

    __show_title: bool
    __show_description: bool
    __scrollable: bool

    _vlayout: QVBoxLayout

    def __init__(
        self,
        item: T,
        fomod_path: Optional[Path],
        flag_names_supplier: FlagNamesSupplier,
        show_title: bool = False,
        show_description: bool = True,
        scrollable: bool = True,
    ) -> None:
        """
        **Note: This constructor is not meant to be overriden by subclasses.**<br>
        **For post-initialization tasks, override `_post_init()` instead.**

        Args:
            item (T): Edited item
            fomod_path (Optional[Path]):
                Path to the FOMOD, if any. Used for validation and display of images.
                Defaults to None.
            flag_names_supplier (FlagNamesSupplier):
                A function that returns an up-to-date list of all flag names from the
                current FOMOD.
            show_title (bool, optional):
                Whether to show the title at the top. Defaults to False.
            show_description (bool, optional):
                Whether to show the description at the top, if any. Defaults to True.
            scrollable (bool, optional):
                Whether to make the widget scrollable. Defaults to True.
        """

        super().__init__()

        self._item = item
        self._fomod_path = fomod_path
        self._flag_names_supplier = flag_names_supplier

        self.__show_title = show_title
        self.__show_description = show_description
        self.__scrollable = scrollable

        self._init_ui()
        self._post_init()

    def _init_ui(self) -> None:
        """
        Initializes the UI of the widget.
        """

        self._vlayout = QVBoxLayout()
        self._vlayout.setContentsMargins(0, 0, 0, 0)
        self._vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        if self.__scrollable:
            scroll_widget = QWidget()
            scroll_widget.setObjectName("transparent")
            scroll_widget.setContentsMargins(0, 0, 0, 0)
            scroll_widget.setLayout(self._vlayout)
            self.setWidget(scroll_widget)
            self.setWidgetResizable(True)
        else:
            self.setLayout(self._vlayout)

        if self.__show_title:
            title_label = QLabel(self.get_title().strip() or self.get_display_name())
            title_label.setObjectName("h2")
            self._vlayout.addWidget(title_label)

        if self.__show_description and self.get_description().strip():
            help_label = QLabel(self.get_description())
            help_label.setWordWrap(True)
            self._vlayout.addWidget(help_label)

    def _post_init(self) -> None:
        """
        This method is called from the constructer right afer `_init_ui()`.
        """

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
