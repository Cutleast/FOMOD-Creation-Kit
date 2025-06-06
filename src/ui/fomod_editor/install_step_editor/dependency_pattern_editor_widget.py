"""
Copyright (c) Cutleast
"""

from pathlib import Path
from typing import override

from PySide6.QtWidgets import QApplication, QLabel

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

    def __init__(self, item: DependencyPattern, fomod_path: Path | None = None) -> None:
        super().__init__(item, fomod_path)

        self.__type_dropdown.currentValueChanged.connect(lambda _: self.changed.emit())
        self.__composite_dependency_editor.changed.connect(self.changed.emit)

    @override
    @classmethod
    def get_display_name(cls) -> str:
        return QApplication.translate(
            "DependencyPatternEditorWidget", "Edit dependency pattern..."
        )

    @override
    def _init_ui(self) -> None:
        super()._init_ui()

        self.__init_header()
        self.__init_type_dropdown()
        self.__init_composite_dependency_editor()

        self.setBaseSize(
            self.__composite_dependency_editor.baseSize().width(),
            self.__composite_dependency_editor.baseSize().height() + 125,
        )

    def __init_header(self) -> None:
        help_label = QLabel(
            self.tr(
                "The plugin has the type specified below when the composite dependency "
                "at the bottom is fulfilled before all other patterns."
            )
        )
        help_label.setWordWrap(True)
        self._vlayout.addWidget(help_label)

    def __init_type_dropdown(self) -> None:
        self.__type_dropdown = EnumDropdown(
            enum_type=PluginType.Type, initial_value=self._item.type.name
        )
        self._vlayout.addWidget(self.__type_dropdown)

    def __init_composite_dependency_editor(self) -> None:
        self.__composite_dependency_editor = CompositeDependencyEditorWidget(
            self._item.dependencies, self._fomod_path
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
