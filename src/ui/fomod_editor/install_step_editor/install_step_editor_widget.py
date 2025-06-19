"""
Copyright (c) Cutleast
"""

from copy import deepcopy
from pathlib import Path
from typing import Optional, Sequence, override

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSplitter,
    QVBoxLayout,
)

from core.fomod.module_config.dependency.composite_dependency import CompositeDependency
from core.fomod.module_config.install_step.group import Group
from core.fomod.module_config.install_step.install_step import InstallStep
from core.fomod.module_config.install_step.visible import Visible
from core.fomod.module_config.plugin.plugin import Plugin
from core.fomod_editor.exceptions import (
    EmptyError,
    NameIsMissingError,
    SpecificEmptyError,
    SpecificValidationError,
)
from ui.widgets.section_area_widget import SectionAreaWidget
from ui.widgets.tree_widget_editor import TreeWidgetEditor

from ..base_editor_widget import BaseEditorWidget
from ..dependency_editor.composite_dependency_editor_widget import (
    CompositeDependencyEditorWidget,
)
from ..editor_dialog import EditorDialog
from .group_editor_widget import GroupEditorWidget
from .plugin_editor_widget import PluginEditorWidget


class InstallStepEditorWidget(BaseEditorWidget[InstallStep]):
    """
    Widget for editing a single install step.
    """

    __groups: list[Group]

    __name_entry: QLineEdit
    __vertical_splitter: QSplitter
    __visibility_label: QLabel
    __visibility_editor_widget: CompositeDependencyEditorWidget
    __horizontal_splitter: QSplitter

    class GroupsTreeWidget(TreeWidgetEditor[Group]):
        """
        Adapted tree widget editor for groups.
        """

        def __init__(self, initial_items: Sequence[Group] = []) -> None:
            super().__init__(initial_items)

            self.changed.connect(
                lambda: self._remove_action.setEnabled(len(self.getItems()) > 1)
            )
            self._remove_action.setEnabled(len(self.getItems()) > 1)

        @override
        def _on_selection_change(self) -> None:
            super()._on_selection_change()

            self._remove_action.setEnabled(
                len(self._tree_widget.selectedItems()) > 0 and len(self.getItems()) > 1
            )

    __groups_tree_widget: GroupsTreeWidget

    class PluginsTreeWidget(TreeWidgetEditor[Plugin]):
        """
        Adapted tree widget editor for plugins.
        """

        def __init__(self, initial_items: Sequence[Plugin] = []) -> None:
            super().__init__(initial_items)

            self.changed.connect(
                lambda: self._remove_action.setEnabled(len(self.getItems()) > 1)
            )
            self._remove_action.setEnabled(len(self.getItems()) > 1)

        @override
        def _on_selection_change(self) -> None:
            super()._on_selection_change()

            self._remove_action.setEnabled(
                len(self._tree_widget.selectedItems()) > 0 and len(self.getItems()) > 1
            )

    __plugins_tree_widget: PluginsTreeWidget

    def __init__(self, item: InstallStep, fomod_path: Path | None = None) -> None:
        self.__groups = deepcopy(item.optional_file_groups.groups)

        super().__init__(item, fomod_path)

        self.__name_entry.textChanged.connect(lambda _: self.changed.emit())
        self.__visibility_editor_widget.changed.connect(self.changed.emit)
        self.__visibility_editor_widget.changed.connect(
            lambda: self.__visibility_label.setText(
                str(self.__visibility_editor_widget.save())
            )
        )

        self.__groups_tree_widget.changed.connect(self.changed.emit)
        self.__groups_tree_widget.onAdd.connect(self.__add_group)
        self.__groups_tree_widget.onEdit.connect(self.__edit_group)
        self.__groups_tree_widget.currentItemChanged.connect(self.__on_group_select)

        self.__plugins_tree_widget.changed.connect(self.changed.emit)
        self.__plugins_tree_widget.changed.connect(self.__on_plugin_change)
        self.__plugins_tree_widget.onAdd.connect(self.__add_plugin)
        self.__plugins_tree_widget.onEdit.connect(self.__edit_plugin)

        if item.optional_file_groups.groups:
            self.__groups_tree_widget.setCurrentItem(
                item.optional_file_groups.groups[0]
            )
        else:
            self.__plugins_tree_widget.setDisabled(True)

    @override
    @classmethod
    def get_display_name(cls) -> str:
        return QApplication.translate("InstallStepEditorWidget", "Edit install step...")

    @override
    @classmethod
    def get_description(cls) -> str:
        return QApplication.translate(
            "InstallStepEditorWidget",
            "An installation step of a FOMOD installer is a single page consisting "
            "of groups of files that can be set to be visible when certain "
            "conditions are met.",
        )

    @override
    def _init_ui(self) -> None:
        super()._init_ui()

        self.__init_name_field()
        self.__init_vertical_splitter()
        self.__init_visibility_editor()
        self.__init_horizontal_splitter()
        self.__init_groups_tree_widget()
        self.__init_plugins_tree_widget()

        self.setBaseSize(1000, 800)

        self.__vertical_splitter.setSizes(
            [100, self.__vertical_splitter.height() - 100]
        )
        self.__vertical_splitter.setHandleWidth(0)

    def __init_name_field(self) -> None:
        hlayout = QHBoxLayout()
        self._vlayout.addLayout(hlayout)

        name_label = QLabel(self.tr("Name:"))
        hlayout.addWidget(name_label)

        self.__name_entry = QLineEdit()
        self.__name_entry.setText(self._item.name)
        hlayout.addWidget(self.__name_entry)

    def __init_vertical_splitter(self) -> None:
        self.__vertical_splitter = QSplitter(Qt.Orientation.Vertical)
        self._vlayout.addWidget(self.__vertical_splitter, stretch=1)

    def __init_visibility_editor(self) -> None:
        visibility_group_box = QGroupBox(self.tr("Visible when"))
        visibility_group_box.setMinimumHeight(100)
        self.__vertical_splitter.addWidget(visibility_group_box)
        self.__vertical_splitter.setCollapsible(0, False)

        vlayout = QVBoxLayout()
        vlayout.setContentsMargins(0, 0, 0, 0)
        visibility_group_box.setLayout(vlayout)

        self.__visibility_label = QLabel(
            str(self._item.visible.dependencies)
            if self._item.visible is not None
            else self.tr("Always visible")
        )

        self.__visibility_editor_widget = CompositeDependencyEditorWidget(
            deepcopy(self._item.visible.dependencies)
            if self._item.visible is not None
            else CompositeDependency()
        )

        section_area_widget = SectionAreaWidget(
            header=self.__visibility_label,
            content=self.__visibility_editor_widget,
            # toggle_position=SectionAreaWidget.TogglePosition.Right,
        )
        section_area_widget.setContentsMargins(0, 0, 0, 0)
        section_area_widget.toggled.connect(
            lambda expanded: (
                visibility_group_box.setMinimumHeight(400 if expanded else 100),
                self.__vertical_splitter.setSizes(
                    [
                        visibility_group_box.minimumHeight(),
                        self.__vertical_splitter.height()
                        - visibility_group_box.minimumHeight(),
                    ]
                ),
                self.__vertical_splitter.setHandleWidth(15 if expanded else 0),
            )
        )
        vlayout.addWidget(section_area_widget)
        section_area_widget.setExpanded(False)

    def __init_horizontal_splitter(self) -> None:
        self.__horizontal_splitter = QSplitter(Qt.Orientation.Horizontal)
        self.__vertical_splitter.addWidget(self.__horizontal_splitter)

    def __init_groups_tree_widget(self) -> None:
        group_box = QGroupBox(self.tr("Optional file groups:"))
        self.__horizontal_splitter.addWidget(group_box)

        group_vlayout = QVBoxLayout()
        group_box.setLayout(group_vlayout)

        self.__groups_tree_widget = InstallStepEditorWidget.GroupsTreeWidget(
            self.__groups
        )
        group_vlayout.addWidget(self.__groups_tree_widget, stretch=1)

    def __init_plugins_tree_widget(self) -> None:
        plugin_box = QGroupBox(self.tr("Plugins:"))
        self.__horizontal_splitter.addWidget(plugin_box)

        plugin_vlayout = QVBoxLayout()
        plugin_box.setLayout(plugin_vlayout)

        self.__plugins_tree_widget = InstallStepEditorWidget.PluginsTreeWidget()
        plugin_vlayout.addWidget(self.__plugins_tree_widget, stretch=1)

    def __add_group(self) -> None:
        group = Group.create()
        dialog: EditorDialog[GroupEditorWidget] = EditorDialog(
            GroupEditorWidget(group, self._fomod_path), validate_on_init=True
        )

        if dialog.exec() == EditorDialog.DialogCode.Accepted:
            self.__groups_tree_widget.addItem(group)

    def __edit_group(self, group: Group) -> None:
        dialog: EditorDialog[GroupEditorWidget] = EditorDialog(
            GroupEditorWidget(group, self._fomod_path)
        )

        if dialog.exec() == EditorDialog.DialogCode.Accepted:
            self.__groups_tree_widget.updateItem(group)

    def __on_group_select(self, group: Optional[Group]) -> None:
        if group is not None:
            self.__plugins_tree_widget.setItems(group.plugins.plugins)
        else:
            self.__plugins_tree_widget.setItems([])

        self.__plugins_tree_widget.setEnabled(group is not None)

    def __add_plugin(self) -> None:
        plugin = Plugin.create()
        dialog: EditorDialog[PluginEditorWidget] = EditorDialog(
            PluginEditorWidget(plugin, self._fomod_path), validate_on_init=True
        )

        if dialog.exec() == EditorDialog.DialogCode.Accepted:
            self.__plugins_tree_widget.addItem(plugin)

    def __edit_plugin(self, plugin: Plugin) -> None:
        dialog: EditorDialog[PluginEditorWidget] = EditorDialog(
            PluginEditorWidget(plugin, self._fomod_path)
        )

        if dialog.exec() == EditorDialog.DialogCode.Accepted:
            self.__plugins_tree_widget.updateItem(plugin)

    def __on_plugin_change(self) -> None:
        current_group: Optional[Group] = self.__groups_tree_widget.getCurrentItem()
        if current_group is not None:
            current_group.plugins.plugins = self.__plugins_tree_widget.getItems()

    @override
    def validate(self) -> None:
        if not self.__name_entry.text().strip():
            raise NameIsMissingError

        try:
            self.__visibility_editor_widget.validate()
        except EmptyError:  # visibility is optional
            pass

        if not self.__groups_tree_widget.getItems():
            raise SpecificEmptyError(self.tr("At least one group must be added!"))

        if not all(
            group.plugins.plugins for group in self.__groups_tree_widget.getItems()
        ):
            raise SpecificValidationError(
                self.tr("Every group must have at least one plugin!")
            )

    @override
    def save(self) -> InstallStep:
        self._item.name = self.__name_entry.text().strip()

        if (visibility := self.__visibility_editor_widget.save()).is_empty():
            self._item.visible = Visible(dependencies=visibility)
        else:
            self._item.visible = None

        self._item.optional_file_groups.groups = self.__groups_tree_widget.getItems()

        self.saved.emit(self._item)
        return self._item
