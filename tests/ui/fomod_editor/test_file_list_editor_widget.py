"""
Copyright (c) Cutleast
"""

import pytest
from pytestqt.qtbot import QtBot

from core.fomod.module_config.file_system.file_list import FileList
from core.fomod_editor.exceptions import EmptyError
from tests.utils import Utils
from ui.fomod_editor.file_list_editor_widget import FileListEditorWidget

from ..ui_test import UiTest


class TestFileListEditorWidget(UiTest):
    """
    Tests `ui.fomod_editor.file_list_editor_widget.FileListEditorWidget`.
    """

    TREE_WIDGET: tuple[str, type[FileListEditorWidget.FileListTreeWidget]] = (
        "tree_widget",
        FileListEditorWidget.FileListTreeWidget,
    )
    """Identifier for accessing the private tree_widget field."""

    @pytest.fixture
    def widget(self, qtbot: QtBot) -> FileListEditorWidget:
        """
        Fixture that creates and provides a FileListEditorWidget instance for tests.
        """

        widget = FileListEditorWidget(FileList(), None, list)
        qtbot.addWidget(widget)
        return widget

    def test_initial_state(self, widget: FileListEditorWidget) -> None:
        """
        Test the initial state of the widget.
        """

        # given
        tree_widget: FileListEditorWidget.FileListTreeWidget = Utils.get_private_field(
            widget, *TestFileListEditorWidget.TREE_WIDGET
        )

        # then
        assert tree_widget.getItems() == []

        with pytest.raises(EmptyError):
            widget.validate()
