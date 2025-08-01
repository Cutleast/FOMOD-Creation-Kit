"""
Copyright (c) Cutleast
"""

import webbrowser
from pathlib import Path

import qtawesome as qta
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMenu, QMenuBar, QMessageBox

from app_context import AppContext
from core.fomod_editor.history import History
from core.utilities.updater import Updater
from ui.widgets.about_dialog import AboutDialog
from ui.widgets.menu import Menu
from ui.widgets.xml_validator_dialog import XmlValidatorDialog

from .settings.settings_dialog import SettingsDialog
from .utilities.icon_provider import get_icon_name_for_palette


class MenuBar(QMenuBar):
    """
    Menu bar for main window.
    """

    create_new_fomod_signal = Signal()
    """Signal emitted when the user clicks on the create new FOMOD button."""

    open_fomod_from_file_signal = Signal()
    """Signal emitted when the user clicks on the open from file button."""

    open_fomod_from_folder_signal = Signal()
    """Signal emitted when the user clicks on the open from folder button."""

    open_recent_fomod_signal = Signal(Path)
    """
    Signal emitted when the user clicks on a recent FOMOD.
    
    Args:
        Path: Path to the FOMOD to open.
    """

    save_fomod_signal = Signal()
    """Signal emitted when the user clicks on the save button."""

    save_fomod_as_signal = Signal()
    """Signal emitted when the user clicks on the save as button."""

    exit_signal = Signal()
    """Signal emitted when the user clicks on the exit button."""

    DISCORD_URL: str = "https://discord.gg/pqEHdWDf8z"
    """URL to our Discord server."""

    NEXUSMODS_URL: str = "https://www.nexusmods.com/site/mods/1366"
    """URL to FCK's Nexus Mods page."""

    GITHUB_URL: str = "https://github.com/Cutleast/FOMOD-Creation-Kit"
    """URL to the GitHub repository."""

    __recent_fomods_menu: QMenu

    def __init__(self, history: History) -> None:
        super().__init__()

        self.__init_file_menu()
        self.__init_extras_menu()
        self.__init_help_menu()

        history.changed.connect(self.__update_recent_fomods_menu)
        self.__update_recent_fomods_menu(history.recent_fomods)

    def __init_file_menu(self) -> None:
        file_menu = Menu(title=self.tr("File"))
        self.addMenu(file_menu)

        new_fomod_action = file_menu.addAction(self.tr("Create new FOMOD installer..."))
        new_fomod_action.setIcon(
            qta.icon("mdi6.plus", color=self.palette().text().color())
        )
        new_fomod_action.setShortcut("Ctrl+N")
        new_fomod_action.triggered.connect(self.create_new_fomod_signal.emit)

        file_menu.addSeparator()

        open_fomod_folder_action = file_menu.addAction(
            self.tr("Load FOMOD installer from folder...")
        )
        open_fomod_folder_action.setIcon(
            qta.icon("mdi6.folder-open", color=self.palette().text().color())
        )
        open_fomod_folder_action.setShortcut("Ctrl+O")
        open_fomod_folder_action.triggered.connect(
            self.open_fomod_from_folder_signal.emit
        )

        open_fomod_file_action = file_menu.addAction(
            self.tr("Load FOMOD installer from file...")
        )
        open_fomod_file_action.setIcon(
            qta.icon("mdi6.folder-open", color=self.palette().text().color())
        )
        open_fomod_file_action.setShortcut("Ctrl+Shift+O")
        open_fomod_file_action.triggered.connect(self.open_fomod_from_file_signal.emit)

        self.__recent_fomods_menu: QMenu = file_menu.addMenu(
            self.tr("Open recent FOMOD installer...")
        )
        self.__recent_fomods_menu.setIcon(
            qta.icon(
                "mdi6.history",
                color=self.palette().text().color(),
                color_disabled="#666666",
            )
        )

        file_menu.addSeparator()

        save_fomod_action = file_menu.addAction(self.tr("Save FOMOD installer"))
        save_fomod_action.setIcon(
            qta.icon("mdi6.content-save", color=self.palette().text().color())
        )
        save_fomod_action.setShortcut("Ctrl+S")
        save_fomod_action.triggered.connect(self.save_fomod_signal.emit)

        save_fomod_as_action = file_menu.addAction(
            self.tr("Save FOMOD installer as...")
        )
        save_fomod_as_action.setIcon(
            qta.icon("mdi6.content-save", color=self.palette().text().color())
        )
        save_fomod_as_action.setShortcut("Ctrl+Shift+S")
        save_fomod_as_action.triggered.connect(self.save_fomod_as_signal.emit)

        file_menu.addSeparator()

        settings_action = file_menu.addAction(self.tr("Settings"))
        settings_action.setIcon(
            qta.icon("mdi6.cog", color=self.palette().text().color())
        )
        settings_action.triggered.connect(self.__open_settings)

        file_menu.addSeparator()

        exit_action = file_menu.addAction(self.tr("Exit"))
        exit_action.setIcon(
            QIcon(":/icons/" + get_icon_name_for_palette("exit", self.palette()))
        )
        exit_action.triggered.connect(self.exit_signal.emit)

    def __update_recent_fomods_menu(self, recent_fomods: list[Path]) -> None:
        self.__recent_fomods_menu.clear()
        self.__recent_fomods_menu.setEnabled(len(recent_fomods) > 0)

        for path in list(reversed(recent_fomods))[:10]:
            self.__add_recent_subaction(self.__recent_fomods_menu, path)

    def __add_recent_subaction(self, recent_menu: QMenu, path: Path) -> None:
        recent_action: QAction = recent_menu.addAction(str(path))
        recent_action.triggered.connect(
            lambda: self.open_recent_fomod_signal.emit(path)
        )

    def __init_extras_menu(self) -> None:
        extras_menu = Menu(title=self.tr("Extras"))
        self.addMenu(extras_menu)

        xml_validator_action = extras_menu.addAction(self.tr("Validate XML file..."))
        xml_validator_action.setIcon(
            qta.icon("mdi6.file-check", color=self.palette().text().color())
        )
        xml_validator_action.triggered.connect(self.__open_xml_validator)

    def __init_help_menu(self) -> None:
        help_menu = Menu(title=self.tr("Help"))
        self.addMenu(help_menu)

        update_action = help_menu.addAction(self.tr("Check for updates..."))
        update_action.setIcon(
            qta.icon("mdi6.refresh", color=self.palette().text().color())
        )
        update_action.triggered.connect(self.__check_for_updates)

        help_menu.addSeparator()

        discord_action = help_menu.addAction(
            self.tr("Get support on our Discord server...")
        )
        discord_action.setIcon(QIcon(":/icons/discord.png"))
        discord_action.setToolTip(MenuBar.DISCORD_URL)
        discord_action.triggered.connect(lambda: webbrowser.open(MenuBar.DISCORD_URL))

        nm_action = help_menu.addAction(self.tr("Open mod page on Nexus Mods..."))
        nm_action.setIcon(QIcon(":/icons/nexus_mods.png"))
        nm_action.setToolTip(MenuBar.NEXUSMODS_URL)
        nm_action.triggered.connect(lambda: webbrowser.open(MenuBar.NEXUSMODS_URL))

        github_action = help_menu.addAction(self.tr("View source code on GitHub..."))
        github_action.setIcon(
            qta.icon("mdi6.github", color=self.palette().text().color())
        )
        github_action.setToolTip(MenuBar.GITHUB_URL)
        github_action.triggered.connect(lambda: webbrowser.open(MenuBar.GITHUB_URL))

        help_menu.addSeparator()

        about_action = help_menu.addAction(self.tr("About"))
        about_action.setIcon(
            qta.icon("fa5s.info-circle", color=self.palette().text().color())
        )
        about_action.triggered.connect(self.__show_about)

        about_qt_action = help_menu.addAction(self.tr("About Qt"))
        about_qt_action.triggered.connect(self.__show_about_qt)

    def __open_settings(self) -> None:
        SettingsDialog(
            AppContext.get_app().app_config,
            AppContext.get_app().behavior_config,
            AppContext.get_app().history,
        ).exec()

    def __open_xml_validator(self) -> None:
        XmlValidatorDialog(AppContext.get_app().main_window).exec()

    def __check_for_updates(self) -> None:
        upd = Updater(AppContext.get_app().APP_VERSION)
        if upd.update_available():
            upd.run()
        else:
            messagebox = QMessageBox(AppContext.get_app().main_window)
            messagebox.setWindowTitle(self.tr("No Updates Available"))
            messagebox.setText(self.tr("There are no updates available."))
            messagebox.setTextFormat(Qt.TextFormat.RichText)
            messagebox.setIcon(QMessageBox.Icon.Information)
            messagebox.exec()

    def __show_about(self) -> None:
        AboutDialog(AppContext.get_app().main_window).exec()

    def __show_about_qt(self) -> None:
        QMessageBox.aboutQt(AppContext.get_app().main_window, self.tr("About Qt"))
