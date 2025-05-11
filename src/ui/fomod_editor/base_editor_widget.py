"""
Copyright (c) Cutleast
"""

from abc import abstractmethod

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QVBoxLayout, QWidget

from core.fomod.fomod import Fomod
from ui.widgets.smooth_scroll_area import SmoothScrollArea


class BaseEditorWidget(SmoothScrollArea):
    """
    Base class for all common editor methods.
    """

    changed = Signal()
    """Signal emitted when the user makes a change to the FOMOD instance."""

    _fomod: Fomod

    _vlayout: QVBoxLayout

    def __init__(self, fomod: Fomod) -> None:
        super().__init__()

        self._fomod = fomod

        self._init_ui()

    def _init_ui(self) -> None:
        scroll_widget = QWidget()
        scroll_widget.setObjectName("transparent")
        self.setWidget(scroll_widget)

        self._vlayout = QVBoxLayout()
        scroll_widget.setLayout(self._vlayout)

    @abstractmethod
    def save(self) -> None:
        """
        Saves the user input to the current FOMOD instance.
        """

    @abstractmethod
    def validate(self) -> None:
        """
        Validates the current FOMOD instance.

        Raises:
            ValidationError: If the FOMOD instance is invalid.
        """
