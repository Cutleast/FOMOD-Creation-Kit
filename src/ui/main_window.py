"""
Copyright (c) Cutleast
"""

from pathlib import Path
from typing import override

from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import QMainWindow

from core.config.app_config import AppConfig
from core.fomod.fomod import Fomod
from core.utilities.logger import Logger

from .main_widget import MainWidget
from .menubar import MenuBar
from .statusbar import StatusBar


class MainWindow(QMainWindow):
    """
    Class for main installer window.
    """

    __menu_bar: MenuBar
    __main_widget: MainWidget
    __status_bar: StatusBar

    def __init__(self, app_config: AppConfig, logger: Logger) -> None:
        super().__init__()

        self.resize(1000, 700)

        self.__init_ui(app_config, logger)

        self.__menu_bar.create_new_fomod_signal.connect(
            self.__main_widget.create_new_fomod
        )
        self.__menu_bar.open_fomod_from_file_signal.connect(
            self.__main_widget.open_fomod_from_file
        )
        self.__menu_bar.open_fomod_from_folder_signal.connect(
            self.__main_widget.open_fomod_from_folder
        )
        self.__menu_bar.save_fomod_signal.connect(self.__main_widget.save_fomod)
        self.__menu_bar.save_fomod_as_signal.connect(self.__main_widget.save_fomod_as)
        self.__menu_bar.exit_signal.connect(self.close)
        self.__main_widget.get_fomod_editor_widget().changed.connect(self.__on_change)

    def __init_ui(self, app_config: AppConfig, logger: Logger) -> None:
        self.__init_menu_bar()
        self.__init_main_widget(app_config)
        self.__init_status_bar(logger)

    def __init_menu_bar(self) -> None:
        self.__menu_bar = MenuBar()
        self.setMenuBar(self.__menu_bar)

    def __init_main_widget(self, app_config: AppConfig) -> None:
        self.__main_widget = MainWidget(app_config)
        self.setCentralWidget(self.__main_widget)

    def __init_status_bar(self, logger: Logger) -> None:
        self.__status_bar = StatusBar(logger)
        self.setStatusBar(self.__status_bar)

    def __on_change(self, fomod: Fomod, unsaved: bool) -> None:
        if unsaved and fomod.path is not None:
            self.setWindowTitle(f"{fomod.path}*")
        elif unsaved:
            self.setWindowTitle(self.tr("Unnamed") + "*")
        elif fomod.path is not None:
            self.setWindowTitle(str(fomod.path))
        else:
            self.setWindowTitle(self.tr("Unnamed"))

    def open_fomod(self, path: Path) -> None:
        """
        Opens the FOMOD installer from the specified path.

        Args:
            path (Path): The path to open a FOMOD installer.
        """

        self.__main_widget.open_fomod(path)

    def create_new_fomod(self) -> None:
        """
        Creates a new FOMOD installer and opens it in the FOMOD editor widget.
        """

        self.__main_widget.create_new_fomod()

    @override
    def closeEvent(self, event: QCloseEvent) -> None:
        if self.__main_widget.close():
            self.__status_bar.close_log_window()

            return super().closeEvent(event)
        else:
            event.ignore()
