"""
Copyright (c) Cutleast
"""

from typing import override

from PySide6.QtWidgets import QApplication

from core.fomod.module_config.dependency.dependency_pattern import DependencyPattern
from core.fomod.module_config.plugin.plugin_type import PluginType
from ui.widgets.enum_dropdown import EnumDropdown

from ..base_editor_widget import BaseEditorWidget
from ..dependency_editor.composite_dependency_editor_widget import (
    CompositeDependencyEditorWidget,
)


class DependencyPatternEditorWidget(BaseEditorWidget[DependencyPattern]):
    """
    Widget for editing a dependency pattern which consists of a composite dependency
    and a plugin type.
    """

    __type_dropdown: EnumDropdown[PluginType.Type]
    __composite_dependency_editor: CompositeDependencyEditorWidget

    @override
    def _post_init(self) -> None:
        self.__type_dropdown.currentValueChanged.connect(lambda _: self.changed.emit())
        self.__composite_dependency_editor.changed.connect(self.changed.emit)

    @override
    @classmethod
    def get_display_name(cls) -> str:
        return QApplication.translate(
            "DependencyPatternEditorWidget", "Edit dependency pattern..."
        )

    @override
    @classmethod
    def get_description(cls) -> str:
        return QApplication.translate(
            "DependencyPatternEditorWidget",
            "The plugin has the type specified below when the composite dependency at "
            "the bottom is fulfilled before all other patterns.",
        )

    @override
    def _init_ui(self) -> None:
        super()._init_ui()

        self.__init_type_dropdown()
        self.__init_composite_dependency_editor()

        self.setBaseSize(
            self.__composite_dependency_editor.baseSize().width(),
            self.__composite_dependency_editor.baseSize().height() + 125,
        )

    def __init_type_dropdown(self) -> None:
        self.__type_dropdown = EnumDropdown(
            enum_type=PluginType.Type, initial_value=self._item.type.name
        )
        self._vlayout.addWidget(self.__type_dropdown)

    def __init_composite_dependency_editor(self) -> None:
        self.__composite_dependency_editor = CompositeDependencyEditorWidget(
            self._item.dependencies, self._fomod_path, self._flag_names_supplier
        )
        self._vlayout.addWidget(self.__composite_dependency_editor)

    @override
    def validate(self) -> None:
        self.__composite_dependency_editor.validate()

    @override
    def save(self) -> DependencyPattern:
        self._item.type.name = self.__type_dropdown.getCurrentValue()
        self._item.dependencies = self.__composite_dependency_editor.save()

        self.saved.emit(self._item)
        return self._item
