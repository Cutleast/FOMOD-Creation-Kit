"""
Copyright (c) Cutleast
"""

import logging
import os
import platform
import subprocess
import sys
import time
from argparse import Namespace
from pathlib import Path
from typing import override

from PySide6.QtCore import QTranslator
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

from core.config.app_config import AppConfig
from core.config.behavior_config import BehaviorConfig
from core.fomod_editor.history import History
from core.utilities.exception_handler import ExceptionHandler
from core.utilities.exe_info import get_current_path
from core.utilities.localisation import Language, detect_system_locale
from core.utilities.logger import Logger
from core.utilities.updater import Updater
from ui.main_window import MainWindow
from ui.utilities.stylesheet_processor import StylesheetProcessor


class App(QApplication):
    """
    Main application class.
    """

    APP_NAME: str = "FOMOD Creation Kit"
    APP_VERSION: str = "development"

    args: Namespace
    app_config: AppConfig
    behavior_config: BehaviorConfig
    history: History

    cur_path: Path = get_current_path()
    data_path: Path = cur_path / "data"
    res_path: Path = cur_path / "res"
    config_path: Path = data_path / "config"

    log: logging.Logger = logging.getLogger("App")
    logger: Logger
    log_path: Path = data_path / "logs"

    main_window: MainWindow
    stylesheet_processor: StylesheetProcessor
    exception_handler: ExceptionHandler

    doc_path: Path

    def __init__(self, args: Namespace) -> None:
        super().__init__()

        self.args = args

    def init(self) -> None:
        """
        Initializes application.
        """

        self.app_config = AppConfig.load(self.config_path)
        self.behavior_config = BehaviorConfig.load(self.config_path)
        self.history = History(self.data_path)

        log_file: Path = self.log_path / time.strftime(self.app_config.log_file_name)
        self.logger = Logger(
            log_file, self.app_config.log_format, self.app_config.log_date_format
        )
        self.logger.setLevel(self.app_config.log_level)

        self.setApplicationName(App.APP_NAME)
        self.setApplicationDisplayName(f"{App.APP_NAME} v{App.APP_VERSION}")
        self.setApplicationVersion(App.APP_VERSION)
        self.setWindowIcon(QIcon(":/icons/icon.svg"))
        self.load_translation()

        self.stylesheet_processor = StylesheetProcessor(self, self.app_config.ui_mode)
        self.exception_handler = ExceptionHandler(self)
        self.main_window = MainWindow(
            self.app_config, self.behavior_config, self.history, self.logger
        )

        self.log_basic_info()
        self.app_config.print_settings_to_log()
        self.log.info("App started.")

    def log_basic_info(self) -> None:
        """
        Logs basic information.
        """

        width = 100
        log_title = f" {App.APP_NAME} ".center(width, "=")
        self.log.info(f"\n{'=' * width}\n{log_title}\n{'=' * width}")
        self.log.info(f"Program Version: {App.APP_VERSION}")
        self.log.info(f"Executed command: {subprocess.list2cmdline(sys.argv)}")
        self.log.info(f"Current Path: {self.cur_path}")
        self.log.info(f"Resource Path: {self.res_path}")
        self.log.info(f"Data Path: {self.data_path}")
        self.log.info(f"Log Path: {self.log_path}")
        self.log.info(
            "Detected Platform: "
            f"{platform.system()} {platform.version()} {platform.architecture()[0]}"
        )

    def load_translation(self) -> None:
        """
        Loads translation for the configured language
        and installs the translator into the app.
        """

        translator = QTranslator(self)

        language: str
        if self.app_config.language == Language.System:
            language = detect_system_locale() or "en_US"
        else:
            language = self.app_config.language.value

        if language != "en_US":
            translator.load(f":/loc/{language}.qm")
            self.installTranslator(translator)

            self.log.info(f"Loaded localisation for {language}.")

    @override
    def exec(self) -> int:  # type: ignore
        """
        Executes application and shows main window.
        """

        try:
            Updater(self.APP_VERSION).run()
        except Exception as ex:
            self.log.warning(f"Failed to check for updates: {ex}", exc_info=ex)

        if self.args.fomod:
            self.main_window.open_fomod(Path(self.args.fomod))
        else:
            self.main_window.create_new_fomod()

        self.main_window.show()

        retcode: int = super().exec()

        self.clean()

        self.log.info("Exiting application...")

        return retcode

    @override
    def exit(self, retcode: int = 0) -> bool:  # type: ignore
        """
        Exits application.

        Returns:
            bool: Whether the application was exited or the user chose to cancel.
        """

        if self.main_window.close():
            super().exit(retcode)
            return True

        return False

    def clean(self) -> None:
        """
        Cleans up and exits application.
        """

        self.log.info("Cleaning...")

        # Clean up log files
        self.logger.clean_log_folder(
            self.log_path,
            self.app_config.log_file_name,
            self.app_config.log_num_of_files,
        )

    def restart_application(self) -> None:
        """
        Restarts the application.
        """

        if self.exit():
            self.log.info("Restarting application...")
            os.startfile(subprocess.list2cmdline(sys.argv))
