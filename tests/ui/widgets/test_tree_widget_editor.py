"""
Copyright (c) Cutleast
"""

from typing import Callable

import pytest
from cutleast_core_lib.core.utilities.reference_dict import ReferenceDict
from cutleast_core_lib.test.setup.clipboard_mock import ClipboardMock
from pydantic import BaseModel
from PySide6.QtGui import QAction
from PySide6.QtWidgets import QTreeWidgetItem
from pytestqt.qtbot import QtBot

from tests.base_test import BaseTest
from tests.utils import Utils
from ui.widgets.tree_widget_editor import TreeWidgetEditor


class TestTreeWidgetEditor(BaseTest):
    """
    Tests `ui.widgets.tree_widget_editor.TreeWidgetEditor`.
    """

    class SampleObject(BaseModel):
        """A simple class to test the TreeWidgetEditor."""

        name: str
        value: str

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
            TreeWidgetEditor(TestTreeWidgetEditor.SampleObject)
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

    def test_cut_item(
        self, widget: TreeWidgetEditor[SampleObject], clipboard: ClipboardMock
    ) -> None:
        """
        Tests cutting an item. This is like copying it and then removing it.
        """

        # given
        item: TestTreeWidgetEditor.SampleObject = TestTreeWidgetEditor.SampleObject(
            name="item", value="value"
        )
        widget.addItem(item)
        widget.setCurrentItem(item)
        cut_method: Callable[[], None] = Utils.get_private_method(
            widget, "cut_cur_item", lambda: None
        )

        # when
        cut_method()

        # then
        assert clipboard.paste() == '{"name":"item","value":"value"}'
        assert widget.getItems() == []

    def test_copy_item(
        self, widget: TreeWidgetEditor[SampleObject], clipboard: ClipboardMock
    ) -> None:
        """
        Tests copying a JSON representation of the current item.
        """

        # given
        item: TestTreeWidgetEditor.SampleObject = TestTreeWidgetEditor.SampleObject(
            name="item", value="value"
        )
        widget.addItem(item)
        widget.setCurrentItem(item)
        copy_method: Callable[[], None] = Utils.get_private_method(
            widget, "copy_cur_item", lambda: None
        )

        # when
        copy_method()

        # then
        assert clipboard.paste() == '{"name":"item","value":"value"}'

    def test_paste_item(
        self, widget: TreeWidgetEditor[SampleObject], clipboard: ClipboardMock
    ) -> None:
        """
        Tests pasting an item from the clipboard by deserializing it from JSON.
        """

        # given
        json_data: str = '{"name":"item","value":"value"}'
        paste_method: Callable[[], None] = Utils.get_private_method(
            widget, "paste_item", lambda: None
        )
        clipboard.copy(json_data)

        # when
        paste_method()

        # then
        assert widget.getItems() == [
            TestTreeWidgetEditor.SampleObject(name="item", value="value")
        ]

        # given
        clipboard.copy("")

        # when (test that it doesn't raise an error)
        paste_method()
