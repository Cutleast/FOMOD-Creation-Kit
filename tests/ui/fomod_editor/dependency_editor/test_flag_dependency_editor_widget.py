"""
Copyright (c) Cutleast
"""

import pytest
from PySide6.QtWidgets import QLineEdit
from pytestqt.qtbot import QtBot

from core.fomod.module_config.dependency.flag_dependency import FlagDependency
from core.fomod_editor.exceptions import NameIsMissingError, ValueIsMissingError
from tests.ui.ui_test import UiTest
from tests.utils import Utils
from ui.fomod_editor.dependency_editor.flag_dependency_editor_widget import (
    FlagDependencyEditorWidget,
)
from ui.widgets.auto_complete_combobox import AutoCompleteCombobox


class TestFlagDependencyEditorWidget(UiTest):
    """
    Tests `ui.fomod_editor.dependency_editor.flag_dependency_editor_widget.FlagDependencyEditorWidget`.
    """

    NAME_ENTRY: tuple[str, type[AutoCompleteCombobox]] = (
        "name_entry",
        AutoCompleteCombobox,
    )
    """Identifier for accessing the private name_entry field."""

    VALUE_ENTRY: tuple[str, type[QLineEdit]] = "value_entry", QLineEdit
    """Identifier for accessing the private value_entry field."""

    @pytest.fixture
    def widget(self, qtbot: QtBot) -> FlagDependencyEditorWidget:
        """
        Fixture that creates and provides a FlagDependencyEditorWidget instance for tests.
        """

        flag_dependency_editor_widget = FlagDependencyEditorWidget(
            FlagDependency(flag="", value=""), None, lambda: ["test1", "test2"]
        )
        qtbot.addWidget(flag_dependency_editor_widget)
        return flag_dependency_editor_widget

    def test_initial_state(self, widget: FlagDependencyEditorWidget) -> None:
        """
        Test the initial state of the widget.
        """

        # given
        name_entry: AutoCompleteCombobox = Utils.get_private_field(
            widget, *TestFlagDependencyEditorWidget.NAME_ENTRY
        )
        value_entry: QLineEdit = Utils.get_private_field(
            widget, *TestFlagDependencyEditorWidget.VALUE_ENTRY
        )

        # then
        assert name_entry.currentText() == ""
        assert name_entry.count() == 2
        assert name_entry.itemText(0) == "test1"
        assert name_entry.itemText(1) == "test2"
        assert value_entry.text() == ""

        with pytest.raises(NameIsMissingError):
            widget.validate()

    def test_validate(self, qtbot: QtBot, widget: FlagDependencyEditorWidget) -> None:
        """
        Tests the validation of the widget.
        """

        # given
        name_entry: AutoCompleteCombobox = Utils.get_private_field(
            widget, *TestFlagDependencyEditorWidget.NAME_ENTRY
        )
        value_entry: QLineEdit = Utils.get_private_field(
            widget, *TestFlagDependencyEditorWidget.VALUE_ENTRY
        )

        # when
        with qtbot.waitSignal(widget.changed, timeout=1000):
            name_entry.setCurrentText("test")

        # then
        with pytest.raises(ValueIsMissingError):
            widget.validate()

        # when
        with qtbot.waitSignal(widget.changed, timeout=1000):
            value_entry.setText("test")

        # then
        widget.validate()
