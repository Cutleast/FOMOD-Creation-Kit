"""
Copyright (c) Cutleast
"""

import logging
from collections.abc import Sequence
from copy import deepcopy
from typing import Optional, override

from cutleast_core_lib.core.utilities.filter import matches_filter
from cutleast_core_lib.core.utilities.reference_dict import ReferenceDict
from cutleast_core_lib.core.utilities.reverse_dict import reverse_dict
from cutleast_core_lib.ui.utilities.icon_provider import IconProvider
from cutleast_core_lib.ui.utilities.tree_widget import (
    get_item_text,
    iter_toplevel_items,
)
from cutleast_core_lib.ui.widgets.search_bar import SearchBar
from pydantic import BaseModel
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QAction, QCursor, QDropEvent, QShortcut
from PySide6.QtWidgets import (
    QHBoxLayout,
    QMenu,
    QToolBar,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)

from core.utilities.clipboard import Clipboard


class TreeWidgetEditor[T: BaseModel](QWidget):
    """
    Tree widget with built-in buttons for adding and removing items and a search bar.
    """

    log: logging.Logger = logging.getLogger("TreeWidgetEditor")

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

    class ContextMenu(QMenu):
        """
        Context menu for the tree widget.
        """

        duplicateRequested = Signal()
        """
        This signal gets emitted when the user presses the Ctrl+D shortcut or clicks on
        the duplicate action.
        """

        cutRequested = Signal()
        """
        This signal gets emitted when the user presses the Ctrl+X shortcut or clicks on
        the cut action.
        """

        copyRequested = Signal()
        """
        This signal gets emitted when the user presses the Ctrl+C shortcut or clicks on
        the copy action.
        """

        pasteRequested = Signal()
        """
        This signal gets emitted when the user presses the Ctrl+V shortcut or clicks on
        the paste action.
        """

        __model_cls: type[T]

        __duplicate_action: QAction
        __copy_action: QAction
        __paste_action: QAction

        def __init__(
            self, model_cls: type[T], parent: Optional[QWidget] = None
        ) -> None:
            super().__init__(parent)

            self.__model_cls = model_cls

            self.__init_ui()

        def __init_ui(self) -> None:
            self.__duplicate_action = self.addAction(
                IconProvider.get_qta_icon("fa6s.clone"), self.tr("Duplicate item")
            )
            self.__duplicate_action.setShortcut("Ctrl+D")
            self.__duplicate_action.triggered.connect(self.duplicateRequested.emit)

            self.addSeparator()

            self.__cut_action = self.addAction(
                IconProvider.get_qta_icon("mdi6.content-cut"), self.tr("Cut item")
            )
            self.__cut_action.setShortcut("Ctrl+X")
            self.__cut_action.triggered.connect(self.cutRequested.emit)

            self.__copy_action = self.addAction(
                IconProvider.get_qta_icon("mdi6.content-copy"), self.tr("Copy item")
            )
            self.__copy_action.setShortcut("Ctrl+C")
            self.__copy_action.triggered.connect(self.copyRequested.emit)

            self.__paste_action = self.addAction(
                IconProvider.get_qta_icon("mdi6.content-paste"), self.tr("Paste item")
            )
            self.__paste_action.setShortcut("Ctrl+V")
            self.__paste_action.triggered.connect(self.pasteRequested.emit)

        def open(self, cur_item: Optional[T]) -> None:
            self.__duplicate_action.setVisible(cur_item is not None)
            self.__cut_action.setVisible(cur_item is not None)
            self.__copy_action.setVisible(cur_item is not None)

            # show paste action only if clipboard contains valid data
            self.__paste_action.setVisible(
                Clipboard.contains_valid_obj(self.__model_cls)
            )

            self.exec(QCursor.pos())

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

    _model_cls: type[T]
    _items: ReferenceDict[T, QTreeWidgetItem]

    _vlayout: QVBoxLayout
    _remove_action: QAction
    _edit_action: QAction
    __search_bar: SearchBar
    _tree_widget: TreeWidget
    _context_menu: ContextMenu
    __duplicate_shortcut: QShortcut
    __cut_shortcut: QShortcut
    __copy_shortcut: QShortcut
    __paste_shortcut: QShortcut

    def __init__(self, model_cls: type[T], initial_items: Sequence[T] = []) -> None:
        """
        Args:
            model_cls (type[T]): Class of the items to add to the tree widget.
            initial_items (Sequence[T], optional):
                Initial list of items to add to the tree widget. Defaults to [].
        """

        super().__init__()

        self._model_cls = model_cls

        self._init_ui()

        self._items = ReferenceDict()
        for item in initial_items:
            self._add_item(item)

        self.__search_bar.searchChanged.connect(self._filter)
        self._tree_widget.itemDoubleClicked.connect(self.__item_double_clicked)
        self._tree_widget.itemSelectionChanged.connect(self._on_selection_change)
        self._tree_widget.itemMoved.connect(self.changed.emit)
        self._tree_widget.customContextMenuRequested.connect(
            lambda: self._context_menu.open(self.getCurrentItem())
        )
        self._context_menu.duplicateRequested.connect(self.__duplicate_cur_item)
        self.__duplicate_shortcut.activated.connect(self.__duplicate_cur_item)
        self._context_menu.cutRequested.connect(self.__cut_cur_item)
        self.__cut_shortcut.activated.connect(self.__cut_cur_item)
        self._context_menu.copyRequested.connect(self.__copy_cur_item)
        self.__copy_shortcut.activated.connect(self.__copy_cur_item)
        self._context_menu.pasteRequested.connect(self.__paste_item)
        self.__paste_shortcut.activated.connect(self.__paste_item)

    def _init_ui(self) -> None:
        self._vlayout = QVBoxLayout()
        self._vlayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._vlayout)

        self.__init_header()
        self.__init_tree_widget()
        self.__init_context_menu()
        self.__init_shortcuts()

    def __init_header(self) -> None:
        hlayout = QHBoxLayout()
        self._vlayout.addLayout(hlayout)

        tool_bar = QToolBar()
        tool_bar.setFixedWidth(132)
        hlayout.addWidget(tool_bar)

        add_action: QAction = tool_bar.addAction(
            IconProvider.get_qta_icon("mdi6.plus"), self.tr("Add new item...")
        )
        add_action.triggered.connect(self.onAdd.emit)

        self._remove_action = tool_bar.addAction(
            IconProvider.get_qta_icon("mdi6.minus"),
            self.tr("Remove selected item(s)...") + " (" + self.tr("Del") + ")",
        )
        self._remove_action.setDisabled(True)
        self._remove_action.setShortcut("Delete")
        self._remove_action.triggered.connect(self.__remove_selected_items)

        self._edit_action = tool_bar.addAction(
            IconProvider.get_qta_icon("mdi6.pencil"),
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
        self._tree_widget.setIndentation(0)
        self._vlayout.addWidget(self._tree_widget)

    def __init_context_menu(self) -> None:
        self._context_menu = TreeWidgetEditor.ContextMenu(self._model_cls, self)
        self._tree_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)

    def __init_shortcuts(self) -> None:
        self.__duplicate_shortcut = QShortcut(
            "Ctrl+D", self, context=Qt.ShortcutContext.WidgetWithChildrenShortcut
        )
        self.__cut_shortcut = QShortcut(
            "Ctrl+X", self, context=Qt.ShortcutContext.WidgetWithChildrenShortcut
        )
        self.__copy_shortcut = QShortcut(
            "Ctrl+C", self, context=Qt.ShortcutContext.WidgetWithChildrenShortcut
        )
        self.__paste_shortcut = QShortcut(
            "Ctrl+V", self, context=Qt.ShortcutContext.WidgetWithChildrenShortcut
        )

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

    def _add_item(self, item: T) -> QTreeWidgetItem:
        """
        Creates a tree widget item for the given item and adds it to the tree widget.
        Does nothing if the item is already in the tree widget.

        Args:
            item (T): Item to add

        Returns:
            QTreeWidgetItem: Tree widget item belonging to the given item
        """

        if item not in self._items:
            tree_widget_item = QTreeWidgetItem([str(item)])
            tree_widget_item.setFlags(
                tree_widget_item.flags() ^ Qt.ItemFlag.ItemIsDropEnabled
            )
            self._tree_widget.addTopLevelItem(tree_widget_item)
            self._items[item] = tree_widget_item

        return self._items[item]

    def __duplicate_cur_item(self) -> None:
        """
        Duplicates the currently selected item, if any.
        """

        cur_item: Optional[T] = self.getCurrentItem()
        if cur_item is not None:
            self._duplicate_item(cur_item)

    def _duplicate_item(self, item: T) -> QTreeWidgetItem:
        """
        Creates a duplicate of the specified item by adding a deep copy to the tree
        widget.

        Args:
            item (T): Item to duplicate

        Returns:
            QTreeWidgetItem: Tree widget item belonging to the duplicated item
        """

        tree_widget_item: QTreeWidgetItem = self._add_item(deepcopy(item))
        self.changed.emit()

        return tree_widget_item

    def __cut_cur_item(self) -> None:
        """
        Serializes the current item to a JSON string and copies it to the clipboard.
        The item is then removed from the list.
        """

        cur_item: Optional[T] = self.getCurrentItem()
        if cur_item is not None:
            Clipboard.copy(cur_item)
            self.removeItem(cur_item)

    def __copy_cur_item(self) -> None:
        """
        Serializes the current item to a JSON string and copies it to the clipboard.
        """

        cur_item: Optional[T] = self.getCurrentItem()
        if cur_item is not None:
            Clipboard.copy(cur_item)

    def __paste_item(self) -> None:
        """
        Attempts to deserialize an item from the clipboard and add it to the list.
        """

        try:
            item: T = Clipboard.paste(self._model_cls)
            self.addItem(item)
        except Exception as ex:
            self.log.debug(f"Failed to paste item: {ex}", exc_info=ex)

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
            self._add_item(item)

    def addItem(self, item: T) -> None:
        """
        Adds the given item to the tree widget. Emits the changed signal if the item is
        new.

        Args:
            item (T): Item to add
        """

        if item not in self._items:
            self._add_item(item)
            self.setCurrentItem(item)
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
