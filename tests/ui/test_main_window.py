"""
Copyright (c) Cutleast
"""

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem
from pytestqt.qtbot import QtBot

from core.config.app_config import AppConfig
from core.utilities.logger import Logger
from tests.utils import Utils
from ui.main_widget import MainWidget
from ui.main_window import MainWindow
from ui.menubar import MenuBar
from ui.statusbar import StatusBar

from .ui_test import UiTest


class TestMainWindow(UiTest):
    """
    Tests `ui.main_window.MainWindow`.
    """

    MENU_BAR: tuple[str, type[MenuBar]] = ("menu_bar", MenuBar)
    """Identifier for accessing the private menu_bar attribute."""

    MAIN_WIDGET: tuple[str, type[MainWidget]] = ("main_widget", MainWidget)
    """Identifier for accessing the private main_widget attribute."""

    STATUS_BAR: tuple[str, type[StatusBar]] = ("status_bar", StatusBar)
    """Identifier for accessing the private status_bar attribute."""

    @pytest.fixture
    def widget(
        self,
        test_fs: FakeFilesystem,
        app_config: AppConfig,
        logger: Logger,
        qtbot: QtBot,
    ) -> MainWindow:
        """
        Fixture to create and provide a MainWindow instance for tests.
        """

        main_window = MainWindow(app_config, logger)
        qtbot.addWidget(main_window)
        main_window.show()
        return main_window

    def test_initial_state(self, test_fs: FakeFilesystem, widget: MainWindow) -> None:
        """
        Tests the initial state of the MainWindow.
        """

        # given
        menu_bar: MenuBar = Utils.get_private_field(widget, *self.MENU_BAR)
        main_widget: MainWidget = Utils.get_private_field(widget, *self.MAIN_WIDGET)
        status_bar: StatusBar = Utils.get_private_field(widget, *self.STATUS_BAR)

        # then
        assert widget.menuBar() is menu_bar
        assert widget.centralWidget() is main_widget
        assert widget.statusBar() is status_bar
