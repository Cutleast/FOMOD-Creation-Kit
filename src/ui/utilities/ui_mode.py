"""
Copyright (c) Cutleast
"""

from typing import override

from PySide6.QtWidgets import QApplication

from core.utilities.localized_enum import LocalizedEnum


class UIMode(LocalizedEnum):
    """
    Enum for UI modes (Dark, Light, System)
    """

    Dark = "Dark"
    Light = "Light"
    System = "System"

    @override
    def get_localized_name(self) -> str:
        locs: dict[UIMode, str] = {
            UIMode.Dark: QApplication.translate("UIMode", "Dark"),
            UIMode.Light: QApplication.translate("UIMode", "Light"),
            UIMode.System: QApplication.translate("UIMode", "System"),
        }

        return locs[self]
