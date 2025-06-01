"""
Copyright (c) Cutleast
"""

from enum import Enum
from typing import Optional

import qtawesome as qta
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QHBoxLayout, QPushButton, QVBoxLayout, QWidget


class SectionAreaWidget(QWidget):
    """
    A collapsible section area with a widget as header and a widget as content.

    The content is collapsed by default after initialization.
    """

    class TogglePosition(Enum):
        """Enum for the position of the toggle button within the header."""

        Left = 0
        """The toggle button is placed to the left of the header widget."""

        Right = 1
        """The toggle button is placed to the right of the header widget."""

    class Direction(Enum):
        """Enum for the possible directions of the collapsible section."""

        Up = 0
        """The content appears above the header."""

        Down = 1
        """The content appears below the header."""

    toggled = Signal(bool)
    """
    Signal emitted when the toggle button is clicked.

    Args:
        bool: The new state of the section: `True` if expanded, `False` if collapsed
    """

    __header_widget: QWidget
    __content_widget: QWidget
    __direction: Direction

    __chevron_down_icon: QIcon
    __chevron_up_icon: QIcon

    __vlayout: QVBoxLayout
    __toggle_button: QPushButton

    def __init__(
        self,
        header: QWidget,
        content: QWidget,
        toggle_position: TogglePosition = TogglePosition.Left,
        direction: Direction = Direction.Down,
        parent: Optional[QWidget] = None,
    ) -> None:
        """
        Args:
            header (QWidget):
                A widget to display in the header, right next to the toggle button.
            content (QWidget): A widget to display in the collapsible content area.
            toggle_position (TogglePosition, optional):
                The position of the toggle button within the header. Defaults to
                TogglePosition.Left.
            direction (Direction, optional):
                The direction of the collapsible section. Defaults to Direction.Down.
            parent (Optional[QWidget], optional): Parent widget. Defaults to None.
        """

        super().__init__(parent)

        self.__header_widget = header
        self.__content_widget = content
        self.__direction = direction

        self.__chevron_down_icon = qta.icon(
            "mdi6.chevron-down", color=self.palette().text().color()
        )
        self.__chevron_up_icon = qta.icon(
            "mdi6.chevron-up", color=self.palette().text().color()
        )

        self.__init_ui(toggle_position)

        self.__toggle_button.toggled.connect(self.__toggle)

    def __init_ui(self, toggle_position: TogglePosition) -> None:
        self.__vlayout = QVBoxLayout()
        if self.__direction == SectionAreaWidget.Direction.Down:
            self.__vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        else:
            self.__vlayout.setAlignment(Qt.AlignmentFlag.AlignBottom)

        self.setLayout(self.__vlayout)

        self.__init_header(toggle_position)
        self.__init_content_widget()

    def __init_header(self, toggle_position: TogglePosition) -> None:
        hlayout = QHBoxLayout()
        self.__vlayout.addLayout(hlayout)

        hlayout.addWidget(self.__header_widget, stretch=1)

        self.__toggle_button = QPushButton()
        self.__toggle_button.setObjectName("toggle_button")
        self.__toggle_button.setIcon(
            self.__chevron_down_icon
            if self.__direction == SectionAreaWidget.Direction.Down
            else self.__chevron_up_icon
        )
        self.__toggle_button.setCheckable(True)
        self.__toggle_button.setChecked(False)
        hlayout.insertWidget(toggle_position.value, self.__toggle_button)

    def __init_content_widget(self) -> None:
        self.__vlayout.insertWidget(self.__direction.value, self.__content_widget)
        self.__content_widget.hide()

    def __toggle(self, expanded: bool) -> None:
        if (expanded and self.__direction == SectionAreaWidget.Direction.Down) or (
            not expanded and self.__direction == SectionAreaWidget.Direction.Up
        ):
            self.__toggle_button.setIcon(self.__chevron_up_icon)
        else:
            self.__toggle_button.setIcon(self.__chevron_down_icon)

        self.__content_widget.setVisible(expanded)
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
        Toggles the expanded state of the section.
        """

        self.__toggle_button.toggle()


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication, QPlainTextEdit

    app = QApplication()

    btn = QPushButton("A button as header")
    widget = SectionAreaWidget(
        header=btn,
        content=QPlainTextEdit(),
        toggle_position=SectionAreaWidget.TogglePosition.Right,
        direction=SectionAreaWidget.Direction.Up,
    )
    btn.clicked.connect(widget.toggle)
    widget.toggled.connect(print)
    # widget.setExpanded(True)
    widget.show()

    app.exec()
