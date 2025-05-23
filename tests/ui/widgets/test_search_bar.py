"""
Copyright (c) Cutleast
"""

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton
from pytestqt.qtbot import QtBot
from utils import Utils

from ui.widgets.search_bar import SearchBar

from ..ui_test import UiTest


class TestSearchBar(UiTest):
    """
    Tests `ui.widgets.search_bar.SearchBar`.
    """

    CS_TOGGLE: tuple[str, type[QPushButton]] = ("cs_toggle", QPushButton)
    """Identifier for accessing the private case sensitivity toggle button."""

    CLEAR_BUTTON: tuple[str, type[QPushButton]] = ("clear_button", QPushButton)
    """Identifier for accessing the private clear button."""

    @pytest.fixture
    def widget(self, qtbot: QtBot) -> SearchBar:
        """
        Fixture to create and provide a SearchBar instance for tests.
        """

        search_bar = SearchBar()
        qtbot.addWidget(search_bar)
        search_bar.show()
        return search_bar

    def test_initial_state(self, widget: SearchBar) -> None:
        """
        Test the initial state of the widget.
        """

        # given
        clear_button: QPushButton = Utils.get_private_field(
            widget, *TestSearchBar.CLEAR_BUTTON
        )
        cs_toggle: QPushButton = Utils.get_private_field(
            widget, *TestSearchBar.CS_TOGGLE
        )

        # then
        assert widget.text() == ""
        assert not widget.getCaseSensitivity()
        assert clear_button.isHidden()
        assert not cs_toggle.isChecked()
        assert cs_toggle.isHidden()

    def test_text_change_updates_buttons(self, widget: SearchBar, qtbot: QtBot) -> None:
        """
        Test that entering text updates the visibility of the clear and toggle buttons.
        """

        # given
        clear_button: QPushButton = Utils.get_private_field(
            widget, *TestSearchBar.CLEAR_BUTTON
        )
        cs_toggle: QPushButton = Utils.get_private_field(
            widget, *TestSearchBar.CS_TOGGLE
        )

        # when
        assert clear_button.isHidden()
        assert cs_toggle.isHidden()
        widget.setText("Search Text")

        # then
        qtbot.waitUntil(lambda: clear_button.isVisible() and cs_toggle.isVisible())

    def test_clear_button_functionality(self, widget: SearchBar, qtbot: QtBot) -> None:
        """
        Test that clicking the clear button clears the text and hides the buttons.
        """

        # given
        clear_button: QPushButton = Utils.get_private_field(
            widget, *TestSearchBar.CLEAR_BUTTON
        )
        cs_toggle: QPushButton = Utils.get_private_field(
            widget, *TestSearchBar.CS_TOGGLE
        )

        # when
        widget.setText("Search Text")
        qtbot.waitUntil(lambda: clear_button.isVisible() and cs_toggle.isVisible())
        qtbot.mouseClick(clear_button, Qt.MouseButton.LeftButton)

        # then
        assert widget.text() == ""
        assert clear_button.isHidden()
        assert cs_toggle.isHidden()

    def test_case_sensitivity_toggle(self, widget: SearchBar, qtbot: QtBot) -> None:
        """
        Test the case sensitivity toggle button.
        """

        # given
        cs_toggle: QPushButton = Utils.get_private_field(
            widget, *TestSearchBar.CS_TOGGLE
        )

        # when
        widget.setText("Search Text")
        qtbot.waitUntil(cs_toggle.isVisible)
        qtbot.mouseClick(cs_toggle, Qt.MouseButton.LeftButton)
        assert cs_toggle.isChecked()
        assert widget.getCaseSensitivity()
        qtbot.mouseClick(cs_toggle, Qt.MouseButton.LeftButton)

        # then
        assert not cs_toggle.isChecked()
        assert not widget.getCaseSensitivity()

    def test_live_mode_signal_emission(self, widget: SearchBar, qtbot: QtBot) -> None:
        """
        Test that the `searchChanged` signal is emitted in live mode.
        """

        # given
        widget.setLiveMode(True)

        # when
        with qtbot.waitSignal(widget.searchChanged, timeout=1000) as signal:
            widget.setText("Live Test")

        # then
        assert signal.args == ["Live Test", False]

    def test_return_pressed_signal(self, widget: SearchBar, qtbot: QtBot) -> None:
        """
        Test that pressing return emits the searchChanged signal in non-live mode.
        """

        # given
        widget.setLiveMode(False)

        # when
        with qtbot.waitSignal(widget.searchChanged, timeout=1000) as signal:
            qtbot.keyPress(widget, Qt.Key.Key_Return)

        # then
        assert signal.args == ["", False]
