"""
Copyright (c) Cutleast
"""

from PySide6.QtWidgets import QWidget

from core.config.app_config import AppConfig


class MainWidget(QWidget):
    """
    Class for main widget.
    """

    app_config: AppConfig

    def __init__(self, app_config: AppConfig) -> None:
        super().__init__()

        self.app_config = app_config

        self.__init_ui()

    def __init_ui(self) -> None: ...
