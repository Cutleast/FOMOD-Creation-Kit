"""
Copyright (c) Cutleast
"""

from collections.abc import Sequence
from typing import Optional, override

import qtawesome as qta
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QDropEvent
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
from core.utilities.reverse_dict import reverse_dict
from ui.utilities.tree_widget import get_item_text, iter_toplevel_items

from .search_bar import SearchBar


class TreeWidgetEditor[T: object](QWidget):
    """
    Tree widget with built-in buttons for adding and removing items and a search bar.

    This is only suitable for mutable objects. Immutable objects like strings are not
    supported by the used `ReferenceDict` and therefore lose the mapping to their
    item within the tree widget when altered outside of this widget.
    """

    class TreeWidget(QTreeWidget):
        """
        Subclass of QTreeWidget that emits a signal when items are reordered per
        drag'n drop.
        """

        itemMoved = Signal()
        """This signal gets emitted when items are reordered."""

        @override
        def dropEvent(self, event: QDropEvent) -> None:
            super().dropEvent(event)
            self.itemMoved.emit()

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

    currentItemChanged = Signal(object)
    """
    This signal gets emitted when the currently selected item changes.

    Args:
        Optional[T]: The new selected item or None if no item is selected
    """

    _items: ReferenceDict[T, QTreeWidgetItem]

    _vlayout: QVBoxLayout
    _remove_action: QAction
    _edit_action: QAction
    __search_bar: SearchBar
    _tree_widget: TreeWidget

    def __init__(self, initial_items: Sequence[T] = []) -> None:
        """
        Args:
            initial_items (Sequence[T], optional):
                Initial list of items to add to the tree widget. Defaults to [].
        """

        super().__init__()

        self._init_ui()

        self._items = ReferenceDict()
        for item in initial_items:
            self.__add_item(item)

        self.__search_bar.searchChanged.connect(self._filter)
        self._tree_widget.itemDoubleClicked.connect(self.__item_double_clicked)
        self._tree_widget.itemSelectionChanged.connect(self._on_selection_change)
        self._tree_widget.itemChanged.connect(lambda item, col: self.changed.emit())
        self._tree_widget.itemMoved.connect(self.changed.emit)

    def _init_ui(self) -> None:
        self._vlayout = QVBoxLayout()
        self._vlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._vlayout)

        self.__init_header()
        self.__init_tree_widget()

    def __init_header(self) -> None:
        hlayout = QHBoxLayout()
        self._vlayout.addLayout(hlayout)

        tool_bar = QToolBar()
        tool_bar.setFixedWidth(140)
        hlayout.addWidget(tool_bar)

        add_action: QAction = tool_bar.addAction(
            qta.icon(
                "mdi6.plus",
                color=self.palette().text().color(),
                color_disabled="#666666",
            ),
            self.tr("Add new item..."),
        )
        add_action.triggered.connect(self.onAdd.emit)

        self._remove_action = tool_bar.addAction(
            qta.icon(
                "mdi6.minus",
                color=self.palette().text().color(),
                color_disabled="#666666",
            ),
            self.tr("Remove selected item(s)...") + " (" + self.tr("Del") + ")",
        )
        self._remove_action.setDisabled(True)
        self._remove_action.setShortcut("Delete")
        self._remove_action.triggered.connect(self.__remove_selected_items)

        self._edit_action = tool_bar.addAction(
            qta.icon(
                "mdi6.pencil",
                color=self.palette().text().color(),
                color_disabled="#666666",
            ),
            self.tr("Edit selected item...") + " (" + self.tr("Double click") + ")",
        )
        self._edit_action.setDisabled(True)
        self._edit_action.triggered.connect(self.__edit_selected_item)

        self.__search_bar = SearchBar()
        hlayout.addWidget(self.__search_bar)

    def __init_tree_widget(self) -> None:
        self._tree_widget = TreeWidgetEditor.TreeWidget()
        self._tree_widget.setTextElideMode(Qt.TextElideMode.ElideMiddle)
        self._tree_widget.setHeaderHidden(True)
        self._tree_widget.setSelectionMode(QTreeWidget.SelectionMode.ExtendedSelection)
        self._tree_widget.setDragDropMode(QTreeWidget.DragDropMode.InternalMove)
        self._vlayout.addWidget(self._tree_widget)

    def __item_double_clicked(self, item: QTreeWidgetItem, column: int) -> None:
        items: dict[QTreeWidgetItem, T] = {
            item: edited_item
            for edited_item, item in self._items.items()
            if item.isSelected()
        }

        self.onEdit.emit(items[item])

    def _on_selection_change(self) -> None:
        self._remove_action.setDisabled(len(self._tree_widget.selectedItems()) == 0)
        self._edit_action.setDisabled(len(self._tree_widget.selectedItems()) == 0)

        items: dict[QTreeWidgetItem, T] = {
            item: edited_item for edited_item, item in self._items.items()
        }

        if self._tree_widget.currentItem() is not None:  # type: ignore
            self.currentItemChanged.emit(items[self._tree_widget.currentItem()])

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

    def __edit_selected_item(self) -> None:
        self.__item_double_clicked(self._tree_widget.currentItem(), 0)

    def _filter(self, text: str, case_sensitive: bool) -> None:
        for item in iter_toplevel_items(self._tree_widget):
            item.setHidden(
                not matches_filter(get_item_text(item), text, case_sensitive)
            )

    def __add_item(self, item: T) -> None:
        if item not in self._items:
            tree_widget_item = QTreeWidgetItem([str(item)])
            tree_widget_item.setFlags(
                tree_widget_item.flags() ^ Qt.ItemFlag.ItemIsDropEnabled
            )
            self._tree_widget.addTopLevelItem(tree_widget_item)
            self._items[item] = tree_widget_item

    def setItems(self, items: Sequence[T]) -> None:
        """
        Sets the items of the tree widget. In contrast to addItem() this method will not
        emit the changed signal.

        Args:
            items (Sequence[T]): Items to set
        """

        self._tree_widget.clear()
        self._items.clear()

        for item in items:
            self.__add_item(item)

    def addItem(self, item: T) -> None:
        """
        Adds the given item to the tree widget. Emits the changed signal if the item is
        new.

        Args:
            item (T): Item to add
        """

        if item not in self._items:
            self.__add_item(item)
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
        Removes the given item from the tree widget. Emits the changed signal if the item
        was in the tree widget.

        Args:
            item (T): Item to remove
        """

        if item in self._items:
            tree_widget_item: QTreeWidgetItem = self._items.pop(item)
            self._tree_widget.takeTopLevelItem(
                self._tree_widget.indexOfTopLevelItem(tree_widget_item)
            )

            self.changed.emit()

    def getCurrentItem(self) -> Optional[T]:
        """
        Returns:
            Optional[T]: The currently selected item or None.
        """

        if self._tree_widget.currentItem() is not None:  # type: ignore
            return reverse_dict(self._items)[self._tree_widget.currentItem()]

    def setCurrentItem(self, item: T) -> None:
        """
        Sets the specified item as the currently selected.
        Does nothing if the item is not in the tree widget.

        Args:
            item (T): Item to select
        """

        if item in self._items:
            self._tree_widget.setCurrentItem(self._items[item])

    def getItems(self) -> list[T]:
        """
        Returns:
            list[T]: List of items currently in the tree widget
        """

        return list(
            sorted(
                self._items.keys(),
                key=lambda item: self._tree_widget.indexOfTopLevelItem(
                    self._items[item]
                ),
            )
        )
