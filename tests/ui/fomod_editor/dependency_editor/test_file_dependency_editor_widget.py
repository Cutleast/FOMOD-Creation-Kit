"""
Copyright (c) Cutleast
"""

import pytest
from PySide6.QtWidgets import QLineEdit
from pytestqt.qtbot import QtBot

from core.fomod.module_config.dependency.file_dependency import FileDependency
from core.fomod_editor.exceptions import FileNameIsMissingError
from tests.ui.ui_test import UiTest
from tests.utils import Utils
from ui.fomod_editor.dependency_editor.file_dependency_editor_widget import (
    FileDependencyEditorWidget,
)
from ui.widgets.enum_dropdown import EnumDropdown


class TestFileDependencyEditorWidget(UiTest):
    """
    Tests `ui.fomod_editor.dependency_editor.file_dependency_editor_widget.FileDependencyEditorWidget`.
    """

    FILE_NAME_ENTRY: tuple[str, type[QLineEdit]] = "file_name_entry", QLineEdit
    """Identifier for accessing the private file_name_entry field."""

    STATE_DROPDOWN: tuple[str, type[EnumDropdown[FileDependency.State]]] = (
        "state_dropdown",
        EnumDropdown[FileDependency.State],
    )
    """Identifier for accessing the private state_dropdown field."""

    @pytest.fixture
    def widget(self, qtbot: QtBot) -> FileDependencyEditorWidget:
        """
        Fixture that creates and provides a FileDependencyEditorWidget instance for
        tests.
        """

        file_dependency_editor_widget = FileDependencyEditorWidget(
            FileDependency(file="", state=FileDependency.State.Active), None
        )
        qtbot.addWidget(file_dependency_editor_widget)
        return file_dependency_editor_widget

    def test_initial_state(self, widget: FileDependencyEditorWidget) -> None:
        """
        Test the initial state of the widget.
        """

        # given
        file_name_entry: QLineEdit = Utils.get_private_field(
            widget, *TestFileDependencyEditorWidget.FILE_NAME_ENTRY
        )
        state_dropdown: EnumDropdown[FileDependency.State] = Utils.get_private_field(
            widget, *TestFileDependencyEditorWidget.STATE_DROPDOWN
        )

        # then
        assert file_name_entry.text() == ""
        assert state_dropdown.getCurrentValue() == FileDependency.State.Active

        with pytest.raises(FileNameIsMissingError):
            widget.validate()

    def test_validate(self, qtbot: QtBot, widget: FileDependencyEditorWidget) -> None:
        """
        Tests the validation of the widget.
        """

        # given
        file_name_entry: QLineEdit = Utils.get_private_field(
            widget, *TestFileDependencyEditorWidget.FILE_NAME_ENTRY
        )
        state_dropdown: EnumDropdown[FileDependency.State] = Utils.get_private_field(
            widget, *TestFileDependencyEditorWidget.STATE_DROPDOWN
        )

        # when
        with qtbot.waitSignal(widget.changed, timeout=1000):
            file_name_entry.setText("test")

        # then
        widget.validate()

        # when
        with qtbot.waitSignal(widget.changed, timeout=1000):
            state_dropdown.setCurrentValue(FileDependency.State.Inactive)

        # then
        widget.validate()
