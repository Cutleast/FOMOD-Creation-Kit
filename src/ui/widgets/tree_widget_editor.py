"""
Copyright (c) Cutleast
"""

from collections.abc import Sequence

import qtawesome as qta
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QHBoxLayout,
    QToolBar,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from core.utilities.filter import matches_filter
from core.utilities.reference_dict import ReferenceDict
from ui.utilities.tree_widget import get_item_text, iter_toplevel_items

from .search_bar import SearchBar


class TreeWidgetEditor[T: object](QWidget):
    """
    Tree widget with built-in buttons for adding and removing items and a search bar.

    This is only suitable for mutable objects. Immutable objects like strings are not
    supported by the used `ReferenceDict` and therefore lose the mapping to their
    item within the tree widget when altered outside of this widget.
    """

    changed = Signal()
    """
    This signal gets emitted when the user adds or removes items from the tree widget.
    """

    onAdd = Signal()
    """This signal gets emitted when the user clicks on the add button."""

    onEdit = Signal(object)
    """
    This signal gets emitted when the user double clicks an item in the tree widget.

    Args:
        T: Item that was double clicked
    """

    _items: ReferenceDict[T, QTreeWidgetItem]

    _vlayout: QVBoxLayout
    _tree_widget: QTreeWidget

    def __init__(self, initial_items: Sequence[T] = []) -> None:
        """
        Args:
            initial_items (Sequence[T], optional):
                Initial list of items to add to the tree widget. Defaults to [].
        """

        super().__init__()

        self._init_ui()

        self._items = ReferenceDict()
        # addItem() can't be taken here as that would emit the changed signal
        for item in initial_items:
            tree_widget_item = QTreeWidgetItem([str(item)])
            self._tree_widget.addTopLevelItem(tree_widget_item)
            self._items[item] = tree_widget_item

        self.__search_bar.searchChanged.connect(self._filter)

    def _init_ui(self) -> None:
        self._vlayout = QVBoxLayout()
        self.setLayout(self._vlayout)

        self.__init_header()
        self.__init_tree_widget()

    def __init_header(self) -> None:
        hlayout = QHBoxLayout()
        self._vlayout.addLayout(hlayout)

        tool_bar = QToolBar()
        hlayout.addWidget(tool_bar)

        add_action: QAction = tool_bar.addAction(
            qta.icon("mdi6.plus", color=self.palette().text().color()),
            self.tr("Add new item..."),
        )
        add_action.triggered.connect(self.onAdd.emit)

        self.__remove_action = tool_bar.addAction(
            qta.icon(
                "mdi6.minus",
                color=self.palette().text().color(),
                color_disabled="#666666",
            ),
            self.tr("Remove selected item(s)..."),
        )
        self.__remove_action.setDisabled(True)
        self.__remove_action.setShortcut("Delete")
        self.__remove_action.triggered.connect(self.__remove_selected_items)

        self.__search_bar = SearchBar()
        hlayout.addWidget(self.__search_bar)

    def __init_tree_widget(self) -> None:
        self._tree_widget = QTreeWidget()
        self._tree_widget.setTextElideMode(Qt.TextElideMode.ElideMiddle)
        self._tree_widget.setHeaderHidden(True)
        self._tree_widget.setSelectionMode(QTreeWidget.SelectionMode.ExtendedSelection)
        self._tree_widget.itemDoubleClicked.connect(self.__item_double_clicked)
        self._tree_widget.itemSelectionChanged.connect(self.__on_selection_change)
        self._vlayout.addWidget(self._tree_widget)

    def __item_double_clicked(self, item: QTreeWidgetItem, column: int) -> None:
        items: dict[QTreeWidgetItem, T] = {
            item: edited_item
            for edited_item, item in self._items.items()
            if item.isSelected()
        }

        self.onEdit.emit(items[item])

    def __on_selection_change(self) -> None:
        self.__remove_action.setDisabled(len(self._tree_widget.selectedItems()) == 0)

    def __remove_selected_items(self) -> None:
        items: dict[QTreeWidgetItem, T] = {
            item: edited_item
            for edited_item, item in self._items.items()
            if item.isSelected()
        }

        for selected_item in self._tree_widget.selectedItems():
            self._tree_widget.takeTopLevelItem(
                self._tree_widget.indexOfTopLevelItem(selected_item)
            )
            self._items.pop(items[selected_item])

        if items:
            self.changed.emit()

    def _filter(self, text: str, case_sensitive: bool) -> None:
        for item in iter_toplevel_items(self._tree_widget):
            item.setHidden(
                not matches_filter(get_item_text(item), text, case_sensitive)
            )

    def addItem(self, item: T) -> None:
        """
        Adds the given item to the tree widget.

        Args:
            item (T): Item to add
        """

        if item not in self._items:
            tree_widget_item = QTreeWidgetItem([str(item)])
            self._tree_widget.addTopLevelItem(tree_widget_item)
            self._items[item] = tree_widget_item

            self.changed.emit()

    def updateItem(self, item: T) -> None:
        """
        Updates the displayed text of the specified item.
        Does nothing if the item is not in the tree widget.

        Args:
            item (T): Item to update
        """

        if item in self._items:
            tree_widget_item: QTreeWidgetItem = self._items[item]
            tree_widget_item.setText(0, str(item))

            self.changed.emit()

    def removeItem(self, item: T) -> None:
        """
        Removes the given item from the tree widget.

        Args:
            item (T): Item to remove
        """

        if item in self._items:
            tree_widget_item: QTreeWidgetItem = self._items.pop(item)
            self._tree_widget.takeTopLevelItem(
                self._tree_widget.indexOfTopLevelItem(tree_widget_item)
            )

            self.changed.emit()

    def getItems(self) -> list[T]:
        """
        Returns:
            list[T]: List of items currently in the tree widget
        """

        return list(self._items.keys())
