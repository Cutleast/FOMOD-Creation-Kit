"""
Copyright (c) Cutleast
"""

import pytest
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QTreeWidgetItem
from pytestqt.qtbot import QtBot

from core.utilities.reference_dict import ReferenceDict
from tests.utils import Utils
from ui.widgets.tree_widget_editor import TreeWidgetEditor

from ..ui_test import UiTest


class TestTreeWidgetEditor(UiTest):
    """
    Tests `ui.widgets.tree_widget_editor.TreeWidgetEditor`.
    """

    class SampleObject:
        """A simple class to test the TreeWidgetEditor."""

        def __init__(self, name: str, value: str) -> None:
            self.name = name
            self.value = value

    ITEMS: tuple[str, type[ReferenceDict[SampleObject, QTreeWidgetItem]]] = (
        "items",
        ReferenceDict,
    )
    """Identifier for accessing the protected items field."""

    REMOVE_ACTION: tuple[str, type[QAction]] = "remove_action", QAction
    """Identifier for accessing the protected remove_action field."""

    TREE_WIDGET: tuple[str, type[TreeWidgetEditor.TreeWidget]] = (
        "tree_widget",
        TreeWidgetEditor.TreeWidget,
    )
    """Identifier for accessing the protected tree_widget field."""

    @pytest.fixture
    def widget(self, qtbot: QtBot) -> TreeWidgetEditor[SampleObject]:
        """
        Fixture that creates and provides a TreeWidgetEditor instance for tests.
        """

        tree_widget_editor: TreeWidgetEditor[TestTreeWidgetEditor.SampleObject] = (
            TreeWidgetEditor()
        )
        qtbot.addWidget(tree_widget_editor)
        return tree_widget_editor

    def test_initial_state(self, widget: TreeWidgetEditor[SampleObject]) -> None:
        """
        Test the initial state of the widget.
        """

        # given
        items: ReferenceDict[TestTreeWidgetEditor.SampleObject, QTreeWidgetItem] = (
            Utils.get_protected_field(widget, *TestTreeWidgetEditor.ITEMS)
        )
        remove_action: QAction = Utils.get_protected_field(
            widget, *TestTreeWidgetEditor.REMOVE_ACTION
        )
        tree_widget: TreeWidgetEditor.TreeWidget = Utils.get_protected_field(
            widget, *TestTreeWidgetEditor.TREE_WIDGET
        )

        # then
        assert len(items) == 0
        assert not remove_action.isEnabled()
        assert widget.getItems() == []
        assert tree_widget.topLevelItemCount() == 0
