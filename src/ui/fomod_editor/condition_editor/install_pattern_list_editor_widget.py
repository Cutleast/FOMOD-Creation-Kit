"""
Copyright (c) Cutleast
"""

from typing import Sequence, override

from PySide6.QtWidgets import QApplication, QLabel, QTreeWidgetItem

from core.fomod.module_config.condition.conditional_install_pattern import (
    ConditionalInstallPattern,
)
from core.fomod.module_config.condition.conditional_install_pattern_list import (
    ConditionalInstallPatternList,
)
from core.fomod.module_config.dependency.composite_dependency import CompositeDependency
from core.fomod.module_config.file_list import FileList
from core.fomod_editor.exceptions import EmptyError
from ui.fomod_editor.editor_dialog import EditorDialog
from ui.widgets.tree_widget_editor import TreeWidgetEditor

from ..base_editor_widget import BaseEditorWidget
from .install_pattern_editor_widget import InstallPatternEditorWidget


class InstallPatternListEditorWidget(BaseEditorWidget[ConditionalInstallPatternList]):
    """
    Widget for editing a conditional install pattern list.
    """

    class InstallPatternTreeWidget(TreeWidgetEditor[ConditionalInstallPattern]):
        """
        Adapted tree widget editor for conditional install patterns.
        """

        def __init__(
            self, initial_items: Sequence[ConditionalInstallPattern] = []
        ) -> None:
            super().__init__()

            for item in initial_items:
                tree_widget_item = QTreeWidgetItem(
                    [str(item.dependencies), str(item.files)]
                )
                self._tree_widget.addTopLevelItem(tree_widget_item)
                self._items[item] = tree_widget_item

        @override
        def _init_ui(self) -> None:
            super()._init_ui()

            self._tree_widget.setHeaderHidden(False)
            self._tree_widget.setHeaderLabels(
                [self.tr("Dependencies"), self.tr("Files")]
            )

        @override
        def addItem(self, item: ConditionalInstallPattern) -> None:
            if item not in self._items:
                tree_widget_item = QTreeWidgetItem(
                    [str(item.dependencies), str(item.files)]
                )
                self._tree_widget.addTopLevelItem(tree_widget_item)
                self._items[item] = tree_widget_item

                self.changed.emit()

        @override
        def updateItem(self, item: ConditionalInstallPattern) -> None:
            if item in self._items:
                tree_widget_item: QTreeWidgetItem = self._items[item]
                tree_widget_item.setText(0, str(item.dependencies))
                tree_widget_item.setText(1, str(item.files))

                self.changed.emit()

    __tree_widget: InstallPatternTreeWidget

    def __init__(self, item: ConditionalInstallPatternList) -> None:
        super().__init__(item)

        self.__tree_widget.changed.connect(self.changed.emit)
        self.__tree_widget.onAdd.connect(self.__add_install_pattern_item)
        self.__tree_widget.onEdit.connect(self.__edit_install_pattern_item)

    @override
    @classmethod
    def get_display_name(cls) -> str:
        return QApplication.translate(
            "InstallPatternListEditorWidget", "Edit conditional install patterns..."
        )

    @override
    def _init_ui(self) -> None:
        super()._init_ui()

        self.__init_header()
        self.__init_tree_widget()

    def __init_header(self) -> None:
        help_label = QLabel(
            self.tr(
                "This list defines patterns of mod files and conditional flags that "
                "determine whether to install specific files."
            )
        )
        self._vlayout.addWidget(help_label)

    def __init_tree_widget(self) -> None:
        self.__tree_widget = InstallPatternListEditorWidget.InstallPatternTreeWidget(
            self._item.patterns
        )
        self._vlayout.addWidget(self.__tree_widget)

    def __add_install_pattern_item(self) -> None:
        item: ConditionalInstallPattern = ConditionalInstallPattern(
            dependencies=CompositeDependency(), files=FileList()
        )
        dialog: EditorDialog[InstallPatternEditorWidget] = EditorDialog(
            InstallPatternEditorWidget(item), validate_on_init=True
        )

        if dialog.exec() == EditorDialog.DialogCode.Accepted:
            self.__tree_widget.addItem(item)

    def __edit_install_pattern_item(self, item: ConditionalInstallPattern) -> None:
        dialog: EditorDialog[InstallPatternEditorWidget] = EditorDialog(
            InstallPatternEditorWidget(item)
        )

        if dialog.exec() == EditorDialog.DialogCode.Accepted:
            self.__tree_widget.updateItem(item)

    @override
    def validate(self) -> None:
        if not self.__tree_widget.getItems():
            raise EmptyError

    @override
    def save(self) -> ConditionalInstallPatternList:
        self._item.patterns = self.__tree_widget.getItems()

        self.saved.emit(self._item)
        return self._item
