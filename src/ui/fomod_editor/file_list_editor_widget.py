"""
Copyright (c) Cutleast
"""

from pathlib import Path
from typing import override

from PySide6.QtWidgets import QApplication, QLabel, QTreeWidgetItem

from core.fomod.module_config.file_list import FileList
from core.fomod.module_config.file_system_item import FileSystemItem
from core.fomod_editor.exceptions import EmptyError
from ui.fomod_editor.editor_dialog import EditorDialog
from ui.fomod_editor.fs_item_editor_widget import FsItemEditorWidget
from ui.widgets.tree_widget_editor import TreeWidgetEditor

from .base_editor_widget import BaseEditorWidget


class FileListEditorWidget(BaseEditorWidget[FileList]):
    """
    Widget for editing a file list.
    """

    class FileListTreeWidget(TreeWidgetEditor[FileSystemItem]):
        """
        Tree widget editor adapted for file system items.
        """

        def __init__(self, initial_items: list[FileSystemItem] = []) -> None:
            super().__init__()

            for item in initial_items:
                tree_widget_item = QTreeWidgetItem(
                    [str(item.source), str(item.destination)]
                )
                self._tree_widget.addTopLevelItem(tree_widget_item)
                self._items[item] = tree_widget_item

        @override
        def _init_ui(self) -> None:
            super()._init_ui()

            self._tree_widget.setHeaderHidden(False)
            self._tree_widget.setHeaderLabels(
                [self.tr("Source"), self.tr("Destination")]
            )

        @override
        def addItem(self, item: FileSystemItem) -> None:
            if item not in self._items:
                tree_widget_item = QTreeWidgetItem(
                    [str(item.source), str(item.destination)]
                )
                self._tree_widget.addTopLevelItem(tree_widget_item)
                self._items[item] = tree_widget_item

                self.changed.emit()

        @override
        def updateItem(self, item: FileSystemItem) -> None:
            if item in self._items:
                tree_widget_item: QTreeWidgetItem = self._items[item]
                tree_widget_item.setText(0, str(item.source))
                tree_widget_item.setText(1, str(item.destination))

                self.changed.emit()

    __tree_widget: FileListTreeWidget

    def __init__(self, item: FileList) -> None:
        super().__init__(item)

        self.__tree_widget.changed.connect(self.changed.emit)
        self.__tree_widget.onAdd.connect(self.__add_filesystem_item)
        self.__tree_widget.onEdit.connect(self.__edit_filesystem_item)

    @override
    @classmethod
    def get_display_name(cls) -> str:
        return QApplication.translate("FileListEditorWidget", "Edit file list...")

    @override
    def _init_ui(self) -> None:
        super()._init_ui()

        self.__init_header()
        self.__init_tree_widget()

    def __init_header(self) -> None:
        help_label = QLabel(
            self.tr(
                "The file list defines how files are copied to the destination folder."
            )
        )
        self._vlayout.addWidget(help_label)

    def __init_tree_widget(self) -> None:
        self.__tree_widget = FileListEditorWidget.FileListTreeWidget(
            self._item.files + self._item.folders
        )
        self._vlayout.addWidget(self.__tree_widget)

    def __add_filesystem_item(self) -> None:
        fs_item = FileSystemItem(source=Path("__default__"))
        dialog: EditorDialog[FsItemEditorWidget] = EditorDialog(
            FsItemEditorWidget(fs_item), validate_on_init=True
        )

        if dialog.exec() == EditorDialog.DialogCode.Accepted:
            self.__tree_widget.addItem(fs_item)

    def __edit_filesystem_item(self, item: FileSystemItem) -> None:
        dialog: EditorDialog[FsItemEditorWidget] = EditorDialog(
            FsItemEditorWidget(item)
        )

        if dialog.exec() == EditorDialog.DialogCode.Accepted:
            self.__tree_widget.updateItem(item)

    @override
    def validate(self) -> None:
        if not self.__tree_widget.getItems():
            raise EmptyError

    @override
    def save(self) -> FileList:
        fs_items: list[FileSystemItem] = self.__tree_widget.getItems()
        file_items: list[FileSystemItem] = list(
            filter(lambda x: x.source.is_file(), fs_items)
        )
        folder_items: list[FileSystemItem] = list(
            filter(lambda x: x.source.is_dir(), fs_items)
        )

        self._item.files = file_items
        self._item.folders = folder_items

        self.saved.emit(self._item)
        return self._item
