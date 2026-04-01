"""
Copyright (c) Cutleast
"""

import webbrowser
from pathlib import Path

from cutleast_core_lib.ui.utilities.icon_provider import IconProvider
from cutleast_core_lib.ui.widgets.menu import Menu
from PySide6.QtCore import Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu, QMenuBar

from core.fomod_editor.history import History


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

    settings_signal = Signal()
    """Signal emitted when the user clicks on the settings button."""

    exit_signal = Signal()
    """Signal emitted when the user clicks on the exit button."""

    updater_signal = Signal()
    """Signal emitted when the user clicks on the updater button."""

    about_signal = Signal()
    """Signal emitted when the user clicks on the about button."""

    about_qt_signal = Signal()
    """Signal emitted when the user clicks on the about Qt button."""

    xml_validator_signal = Signal()
    """Signal emitted when the user clicks on the XML validator button."""

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
        new_fomod_action.setIcon(IconProvider.get_qta_icon("mdi6.plus"))
        new_fomod_action.setShortcut("Ctrl+N")
        new_fomod_action.triggered.connect(self.create_new_fomod_signal.emit)

        file_menu.addSeparator()

        open_fomod_folder_action = file_menu.addAction(
            self.tr("Load FOMOD installer from folder...")
        )
        open_fomod_folder_action.setIcon(IconProvider.get_qta_icon("mdi6.folder-open"))
        open_fomod_folder_action.setShortcut("Ctrl+O")
        open_fomod_folder_action.triggered.connect(
            self.open_fomod_from_folder_signal.emit
        )

        open_fomod_file_action = file_menu.addAction(
            self.tr("Load FOMOD installer from file...")
        )
        open_fomod_file_action.setIcon(IconProvider.get_qta_icon("mdi6.folder-open"))
        open_fomod_file_action.setShortcut("Ctrl+Shift+O")
        open_fomod_file_action.triggered.connect(self.open_fomod_from_file_signal.emit)

        self.__recent_fomods_menu: QMenu = file_menu.addMenu(
            self.tr("Open recent FOMOD installer...")
        )
        self.__recent_fomods_menu.setIcon(IconProvider.get_qta_icon("mdi6.history"))

        file_menu.addSeparator()

        save_fomod_action = file_menu.addAction(self.tr("Save FOMOD installer"))
        save_fomod_action.setIcon(IconProvider.get_qta_icon("mdi6.content-save"))
        save_fomod_action.setShortcut("Ctrl+S")
        save_fomod_action.triggered.connect(self.save_fomod_signal.emit)

        save_fomod_as_action = file_menu.addAction(
            self.tr("Save FOMOD installer as...")
        )
        save_fomod_as_action.setIcon(IconProvider.get_qta_icon("mdi6.content-save"))
        save_fomod_as_action.setShortcut("Ctrl+Shift+S")
        save_fomod_as_action.triggered.connect(self.save_fomod_as_signal.emit)

        file_menu.addSeparator()

        settings_action = file_menu.addAction(self.tr("Settings"))
        settings_action.setIcon(IconProvider.get_qta_icon("mdi6.cog"))
        settings_action.triggered.connect(self.settings_signal.emit)

        file_menu.addSeparator()

        exit_action = file_menu.addAction(self.tr("Exit"))
        exit_action.setIcon(IconProvider.get_icon("exit"))
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
        xml_validator_action.setIcon(IconProvider.get_qta_icon("mdi6.file-check"))
        xml_validator_action.triggered.connect(self.xml_validator_signal.emit)

    def __init_help_menu(self) -> None:
        help_menu = Menu(title=self.tr("Help"))
        self.addMenu(help_menu)

        update_action = help_menu.addAction(self.tr("Check for updates..."))
        update_action.setIcon(IconProvider.get_qta_icon("mdi6.refresh"))
        update_action.triggered.connect(self.updater_signal.emit)

        help_menu.addSeparator()

        discord_action = help_menu.addAction(
            self.tr("Get support on our Discord server...")
        )
        discord_action.setIcon(IconProvider.get_icon("discord"))
        discord_action.setToolTip(MenuBar.DISCORD_URL)
        discord_action.triggered.connect(lambda: webbrowser.open(MenuBar.DISCORD_URL))

        nm_action = help_menu.addAction(self.tr("Open mod page on Nexus Mods..."))
        nm_action.setIcon(IconProvider.get_icon("nexus_mods"))
        nm_action.setToolTip(MenuBar.NEXUSMODS_URL)
        nm_action.triggered.connect(lambda: webbrowser.open(MenuBar.NEXUSMODS_URL))

        github_action = help_menu.addAction(self.tr("View source code on GitHub..."))
        github_action.setIcon(IconProvider.get_qta_icon("mdi6.github"))
        github_action.setToolTip(MenuBar.GITHUB_URL)
        github_action.triggered.connect(lambda: webbrowser.open(MenuBar.GITHUB_URL))

        help_menu.addSeparator()

        about_action = help_menu.addAction(self.tr("About"))
        about_action.setIcon(IconProvider.get_qta_icon("fa5s.info-circle"))
        about_action.triggered.connect(self.about_signal.emit)

        about_qt_action = help_menu.addAction(self.tr("About Qt"))
        about_qt_action.setIcon(IconProvider.get_icon("qt"))
        about_qt_action.triggered.connect(self.about_qt_signal.emit)
