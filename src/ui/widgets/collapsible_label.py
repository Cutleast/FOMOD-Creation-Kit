"""
Copyright (c) Cutleast
"""

from typing import Optional, override

from cutleast_core_lib.ui.utilities.icon_provider import IconProvider
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon, QResizeEvent
from PySide6.QtWidgets import QLabel, QPushButton, QSizePolicy, QWidget


class CollapsibleLabel(QLabel):
    """
    A label widget that can be collapsed and expanded.
    """

    MAX_HEIGHT: int = 16777215
    """The maximum height the label can have when expanded."""

    toggled = Signal(bool)
    """
    Signal emitted when the label is collapsed or expanded.

    Args:
        bool: `True` if expanded, `False` if collapsed.
    """

    __text: str = ""
    __treshold: int

    __expand_icon: QIcon
    __collapse_icon: QIcon
    __toggle_button: QPushButton

    def __init__(
        self,
        text: Optional[str] = None,
        parent: Optional[QWidget] = None,
        treshold: int = 200,
    ) -> None:
        super().__init__(parent)

        self.__treshold = treshold
        self.__expand_icon = IconProvider.get_icon("arrow_down")
        self.__collapse_icon = IconProvider.get_icon("arrow_up")

        self.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setWordWrap(True)

        self.__init_ui()

        self.__toggle_button.toggled.connect(self.__toggle)

        if text is not None:
            self.setText(text)

        self.adjustSize()

    def __init_ui(self) -> None:
        self.__toggle_button = QPushButton(self)
        self.__toggle_button.setObjectName("toggle_button")
        self.__toggle_button.setIcon(self.__collapse_icon)
        self.__toggle_button.setCheckable(True)
        self.__toggle_button.setChecked(True)
        self.__toggle_button.setFixedSize(39, 36)
        self.__toggle_button.show()

    @override
    def resizeEvent(self, e: QResizeEvent) -> None:
        super().resizeEvent(e)

        self.__update_button_position()

    def __update_button_position(self) -> None:
        self.__toggle_button.move(self.width() - self.__toggle_button.width(), 0)

    def __toggle(self, expanded: bool) -> None:
        if expanded:
            self.__toggle_button.setIcon(self.__collapse_icon)
            self.__toggle_button.setToolTip(self.tr("Reduce"))
            self.setMinimumHeight(0)
            self.setMaximumHeight(CollapsibleLabel.MAX_HEIGHT)
            self.setSizePolicy(
                self.sizePolicy().horizontalPolicy(), QSizePolicy.Policy.Minimum
            )
        else:
            self.__toggle_button.setIcon(self.__expand_icon)
            self.__toggle_button.setToolTip(self.tr("Expand"))

            if self.__toggle_button.isVisible():
                self.setFixedHeight(self.__toggle_button.height())
            else:
                self.setMinimumHeight(0)

        self.setProperty("expanded", expanded)
        self.style().unpolish(self)
        self.style().polish(self)
        self.toggled.emit(expanded)

        self.__update_text()

    @override
    def setText(self, text: str) -> None:
        self.__text = text
        self.__update_text()

        expandable: bool = len(text) > self.__treshold
        self.__toggle_button.setVisible(expandable)
        self.setProperty("expandable", expandable)

    def __update_text(self) -> None:
        if not self.isExpanded() and len(self.__text) > self.__treshold:
            return super().setText(self.__text[: self.__treshold] + "...")

        super().setText(self.__text)

    @override
    def text(self) -> str:
        return self.__text

    def setExpanded(self, expanded: bool) -> None:
        """
        Sets the expanded state of the label.

        Args:
            expanded (bool): Whether the label should be expanded.
        """

        self.__toggle_button.setChecked(expanded)

    def isExpanded(self) -> bool:
        """
        Returns:
            bool: Whether the label is currently expanded.
        """

        return self.__toggle_button.isChecked()

    def toggle(self) -> None:
        """
        Toggles the expanded state of the label.
        """

        self.__toggle_button.toggle()


if __name__ == "__main__":
    import os
    import sys

    from cutleast_core_lib.ui.utilities.ui_mode import UIMode
    from PySide6.QtWidgets import QApplication, QVBoxLayout

    sys.path.append(os.path.join(os.getcwd(), "src"))

    import resources_rc as resources_rc

    IconProvider(UIMode.Dark, "#ffffff")

    app = QApplication()

    window = QWidget()
    layout = QVBoxLayout()
    window.setLayout(layout)

    label = CollapsibleLabel("Lorem ipsum dolor sit amet")
    label.setWordWrap(True)
    layout.addWidget(label)

    layout.addStretch()

    window.show()
    app.exec()
