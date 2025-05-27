"""
Copyright (c) Cutleast
"""

from typing import override

from PySide6.QtWidgets import QApplication

from core.fomod.module_config.condition.conditional_install_pattern import (
    ConditionalInstallPattern,
)

from ..base_editor_widget import BaseEditorWidget
from ..dependency_editor.composite_dependency_editor_widget import (
    CompositeDependencyEditorWidget,
)
from ..file_list_editor_widget import FileListEditorWidget


class InstallPatternEditorWidget(BaseEditorWidget[ConditionalInstallPattern]):
    """
    Widget for editing a conditional install pattern.
    """

    __dependency_editor_widget: CompositeDependencyEditorWidget
    __file_list_editor_widget: FileListEditorWidget

    def __init__(self, item: ConditionalInstallPattern) -> None:
        super().__init__(item)

        self.__dependency_editor_widget.changed.connect(self.changed.emit)
        self.__file_list_editor_widget.changed.connect(self.changed.emit)

    @override
    @classmethod
    def get_display_name(cls) -> str:
        return QApplication.translate(
            "InstallPatternEditorWidget", "Edit conditional install pattern..."
        )

    @override
    def _init_ui(self) -> None:
        super()._init_ui()

        self.__init_dependency_editor_widget()
        self.__init_file_list_editor_widget()

        self.setBaseSize(800, 800)

    def __init_dependency_editor_widget(self) -> None:
        self.__dependency_editor_widget = CompositeDependencyEditorWidget(
            self._item.dependencies
        )
        self._vlayout.addWidget(self.__dependency_editor_widget)

    def __init_file_list_editor_widget(self) -> None:
        self.__file_list_editor_widget = FileListEditorWidget(self._item.files)
        self._vlayout.addWidget(self.__file_list_editor_widget)

    @override
    def validate(self) -> None:
        self.__dependency_editor_widget.validate()
        self.__file_list_editor_widget.validate()

    @override
    def save(self) -> ConditionalInstallPattern:
        self._item.dependencies = self.__dependency_editor_widget.save()
        self._item.files = self.__file_list_editor_widget.save()

        self.saved.emit(self._item)
        return self._item
