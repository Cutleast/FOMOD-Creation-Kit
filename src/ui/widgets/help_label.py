"""
Copyright (c) Cutleast
"""

from typing import override

import qtawesome as qta
from PySide6.QtCore import QEvent
from PySide6.QtGui import QEnterEvent
from PySide6.QtWidgets import QLabel


class HelpLabel(QLabel):
    """
    A label that displays help text when hovered over.
    """

    def __init__(self, help_text: str) -> None:
        super().__init__(help_text)

        self.setToolTip(help_text)
        self.setPixmap(
            qta.icon("mdi6.information", color=self.palette().text().color()).pixmap(
                24, 24
            )
        )

    @override
    def enterEvent(self, event: QEnterEvent) -> None:
        super().enterEvent(event)

        self.setPixmap(
            qta.icon("mdi6.information", color=self.palette().accent().color()).pixmap(
                24, 24
            )
        )

    @override
    def leaveEvent(self, event: QEvent) -> None:
        super().leaveEvent(event)

        self.setPixmap(
            qta.icon("mdi6.information", color=self.palette().text().color()).pixmap(
                24, 24
            )
        )
