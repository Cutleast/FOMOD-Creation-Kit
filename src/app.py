"""
Copyright (c) Cutleast
"""

import os
import sys
from argparse import Namespace
from pathlib import Path
from typing import Optional, cast, override

from cutleast_core_lib.base_app import BaseApp
from cutleast_core_lib.core.utilities.localisation import detect_system_locale
from cutleast_core_lib.core.utilities.singleton import Singleton
from PySide6.QtCore import QTranslator
from PySide6.QtGui import QIcon

import resources_rc as resources_rc
from core.config.app_config import AppConfig
from core.config.behavior_config import BehaviorConfig
from core.fomod_editor.history import History
from ui.main_window import MainWindow
from ui.utilities.theme_manager import ThemeManager


class App(BaseApp, Singleton):
    """
    Main application class.
    """

    APP_NAME: str = "FOMOD Creation Kit"
    APP_VERSION: str = "development"

    behavior_config: BehaviorConfig
    history: History

    doc_path: Path

    def __init__(self, args: Namespace) -> None:
        Singleton.__init__(self)
        super().__init__(args)

    @override
    def _init(self) -> None:
        self.setApplicationName(App.APP_NAME)
        self.setApplicationDisplayName(f"{App.APP_NAME} v{App.APP_VERSION}")
        self.setApplicationVersion(App.APP_VERSION)
        self.setWindowIcon(QIcon(":/icons/icon.svg"))

        super()._init()

    @override
    def _load_app_config(self) -> AppConfig:
        return AppConfig.load(self.config_path)

    @override
    def _get_theme_manager(self) -> Optional[ThemeManager]:
        return ThemeManager(
            self.app_config.accent_color,
            self.app_config.ui_mode,
            fonts=[":/fonts/Outfit-VariableFont_wght.ttf"],
        )

    @override
    def _init_main_window(self) -> MainWindow:
        self.__load_translation()

        self.behavior_config = BehaviorConfig.load(self.config_path)
        self.history = History(self.data_path)

        return MainWindow(
            app_config=cast(AppConfig, self.app_config),
            behavior_config=self.behavior_config,
            history=self.history,
            logger=self.logger,
        )

    def __load_translation(self) -> None:
        """
        Loads translation for the configured language and installs the translator into
        the app.
        """

        translator = QTranslator(self)

        app_config: AppConfig = cast(AppConfig, self.app_config)

        language: str
        if app_config.language == AppConfig.AppLanguage.System:
            language = detect_system_locale() or "en_US"
        else:
            language = app_config.language.value

        if language != "en_US":
            res_file: str = f":/loc/{language}.qm"
            if not translator.load(res_file):
                self.log.error(
                    f"Failed to load localisation for {language} from '{res_file}'."
                )
            else:
                self.installTranslator(translator)
                self.log.info(f"Loaded localisation for {language}.")

    @override
    def exec(self) -> int:  # pyright: ignore[reportIncompatibleMethodOverride]
        main_window: MainWindow = cast(MainWindow, self.main_window)
        if self.args.fomod:
            main_window.open_fomod(Path(self.args.fomod))
        else:
            main_window.create_new_fomod()

        return super().exec()

    def restart_application(self) -> None:
        """
        Restarts the application with the current open FOMOD, if any.
        """

        if self.exit():
            fomod_path: Optional[Path] = None
            if (
                fomod := cast(MainWindow, self.main_window).get_fomod()
            ) is not None and fomod.path is not None:
                fomod_path = fomod.path

            if fomod_path is not None:
                self.log.info(f"Restarting application with FOMOD '{fomod_path}'...")
                os.startfile(sys.argv[0], arguments=f'"{fomod_path}"')
            else:
                self.log.info("Restarting application...")
                os.startfile(sys.argv[0])

    @override
    @classmethod
    def get_repo_owner(cls) -> Optional[str]:
        return "Cutleast"

    @override
    @classmethod
    def get_repo_name(cls) -> Optional[str]:
        return "FOMOD-Creation-Kit"

    @override
    @classmethod
    def get_repo_branch(cls) -> Optional[str]:
        return "master"
