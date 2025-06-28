"""
Copyright (c) Cutleast
"""

from collections.abc import Sequence
from typing import override

from PySide6.QtWidgets import QApplication, QHBoxLayout, QLabel, QTreeWidgetItem

from core.fomod.module_config.dependency.default_plugin_type import DefaultPluginType
from core.fomod.module_config.dependency.dependency_pattern import DependencyPattern
from core.fomod.module_config.dependency.dependency_plugin_type import (
    DependencyPluginType,
)
from core.fomod_editor.exceptions import SpecificEmptyError
from ui.widgets.enum_dropdown import EnumDropdown
from ui.widgets.tree_widget_editor import TreeWidgetEditor

from ..base_editor_widget import BaseEditorWidget
from ..editor_dialog import EditorDialog
from .dependency_pattern_editor_widget import DependencyPatternEditorWidget


class DependencyPluginTypeEditorWidget(BaseEditorWidget[DependencyPluginType]):
    """
    Widget for editing a plugin type that is dependent upon the state of other mods.
    """

    __default_type_selector: EnumDropdown[DefaultPluginType.Type]

    class PatternTreeWidget(TreeWidgetEditor[DependencyPattern]):
        """
        Tree widget editor adapted for dependency patterns.
        """

        def __init__(self, initial_items: Sequence[DependencyPattern] = []) -> None:
            super().__init__()

            for item in initial_items:
                tree_widget_item = QTreeWidgetItem(
                    [str(item.dependencies), str(item.type)]
                )
                self._tree_widget.addTopLevelItem(tree_widget_item)
                self._items[item] = tree_widget_item

        @override
        def _init_ui(self) -> None:
            super()._init_ui()

            self._tree_widget.setHeaderHidden(False)
            self._tree_widget.setHeaderLabels(
                [self.tr("Dependencies"), self.tr("Type")]
            )
            self._tree_widget.header().resizeSection(0, 400)

        @override
        def addItem(self, item: DependencyPattern) -> None:
            if item not in self._items:
                tree_widget_item = QTreeWidgetItem(
                    [str(item.dependencies), str(item.type)]
                )
                self._tree_widget.addTopLevelItem(tree_widget_item)
                self._items[item] = tree_widget_item

                self.changed.emit()

        @override
        def updateItem(self, item: DependencyPattern) -> None:
            if item in self._items:
                tree_widget_item: QTreeWidgetItem = self._items[item]
                tree_widget_item.setText(0, str(item.dependencies))
                tree_widget_item.setText(1, str(item.type))

                self.changed.emit()

    __pattern_tree_widget: PatternTreeWidget

    @override
    def _post_init(self) -> None:
        self.__default_type_selector.currentValueChanged.connect(
            lambda _: self.changed.emit()
        )
        self.__pattern_tree_widget.changed.connect(self.changed.emit)

        self.__pattern_tree_widget.onAdd.connect(self.__add_pattern)
        self.__pattern_tree_widget.onEdit.connect(self.__edit_pattern)

    @override
    @classmethod
    def get_display_name(cls) -> str:
        return QApplication.translate(
            "DependencyPluginTypeEditorWidget", "Edit dependency plugin type..."
        )

    @override
    def _init_ui(self) -> None:
        super()._init_ui()

        self.__init_default_type_selector()
        self.__init_pattern_tree_widget()

    def __init_default_type_selector(self) -> None:
        hlayout = QHBoxLayout()
        self._vlayout.addLayout(hlayout)

        default_type_label = QLabel(
            self.tr("Default type (if no pattern below matches):")
        )
        hlayout.addWidget(default_type_label)

        self.__default_type_selector = EnumDropdown(
            enum_type=DefaultPluginType.Type, initial_value=self._item.default_type.name
        )
        hlayout.addWidget(self.__default_type_selector)

    def __init_pattern_tree_widget(self) -> None:
        self.__pattern_tree_widget = DependencyPluginTypeEditorWidget.PatternTreeWidget(
            self._item.patterns.patterns
        )
        self._vlayout.addWidget(self.__pattern_tree_widget)

    def __add_pattern(self) -> None:
        item = DependencyPattern.create()
        dialog: EditorDialog[DependencyPatternEditorWidget] = EditorDialog(
            DependencyPatternEditorWidget(item, self._fomod_path), validate_on_init=True
        )

        if dialog.exec() == EditorDialog.DialogCode.Accepted:
            self.__pattern_tree_widget.addItem(item)

    def __edit_pattern(self, item: DependencyPattern) -> None:
        dialog: EditorDialog[DependencyPatternEditorWidget] = EditorDialog(
            DependencyPatternEditorWidget(item, self._fomod_path)
        )

        if dialog.exec() == EditorDialog.DialogCode.Accepted:
            self.__pattern_tree_widget.updateItem(item)

    @override
    def validate(self) -> None:
        if not self.__pattern_tree_widget.getItems():
            raise SpecificEmptyError(
                self.tr("At least one pattern has to be specified!")
            )

    @override
    def save(self) -> DependencyPluginType:
        self._item.default_type = DefaultPluginType(
            name=self.__default_type_selector.getCurrentValue()
        )
        self._item.patterns.patterns = self.__pattern_tree_widget.getItems()

        self.saved.emit(self._item)
        return self._item
