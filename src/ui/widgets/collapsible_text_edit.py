"""
Copyright (c) Cutleast
"""

from typing import Optional, override

import qtawesome as qta
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon, QResizeEvent
from PySide6.QtWidgets import QPlainTextEdit, QPushButton, QSizePolicy, QWidget


class CollapsibleTextEdit(QPlainTextEdit):
    """
    A text edit widget that can be collapsed and expanded.
    """

    MAX_HEIGHT: int = 16777215
    """The maximum height the text edit can have when expanded."""

    toggled = Signal(bool)
    """
    Signal emitted when the text edit is collapsed or expanded.

    Args:
        bool: `True` if expanded, `False` if collapsed.
    """

    __expand_icon: QIcon
    __collapse_icon: QIcon
    __toggle_button: QPushButton

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.__expand_icon = qta.icon(
            "mdi6.chevron-down", color=self.palette().text().color(), scale_factor=1.2
        )
        self.__collapse_icon = qta.icon(
            "mdi6.chevron-up", color=self.palette().text().color(), scale_factor=1.2
        )

        self.__init_ui()

        self.__toggle_button.toggled.connect(self.__toggle)

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
            self.setMinimumHeight(70)
            self.setMaximumHeight(CollapsibleTextEdit.MAX_HEIGHT)
            self.setSizePolicy(
                self.sizePolicy().horizontalPolicy(), QSizePolicy.Policy.Expanding
            )
            self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        else:
            self.__toggle_button.setIcon(self.__expand_icon)
            self.__toggle_button.setToolTip(self.tr("Expand"))
            self.setFixedHeight(36)
            self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
            self.verticalScrollBar().setValue(0)

        self.setProperty("expanded", expanded)
        self.style().unpolish(self)
        self.style().polish(self)
        self.toggled.emit(expanded)

    def setExpanded(self, expanded: bool) -> None:
        """
        Sets the expanded state of the section.

        Args:
            expanded (bool): Whether the section should be expanded.
        """

        self.__toggle_button.setChecked(expanded)

    def isExpanded(self) -> bool:
        """
        Returns:
            bool: Whether the section is currently expanded.
        """

        return self.__toggle_button.isChecked()

    def toggle(self) -> None:
        """
        Toggles the expanded state of the text edit.
        """

        self.__toggle_button.toggle()


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication, QVBoxLayout

    app = QApplication()

    window = QWidget()
    layout = QVBoxLayout()
    window.setLayout(layout)

    layout.addWidget(CollapsibleTextEdit())

    layout.addStretch()

    window.show()
    app.exec()
