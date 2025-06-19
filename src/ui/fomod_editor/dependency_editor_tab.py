"""
Copyright (c) Cutleast
"""

from pathlib import Path
from typing import Optional, override

from PySide6.QtWidgets import QApplication

from core.fomod.module_config.dependency.composite_dependency import CompositeDependency
from core.fomod_editor.exceptions import EmptyError

from .base_editor_widget import BaseEditorWidget
from .dependency_editor.composite_dependency_editor_widget import (
    CompositeDependencyEditorWidget,
)


class DependencyEditorTab(BaseEditorWidget[CompositeDependency]):
    """
    Widget class for editing the module dependencies of a FOMOD installer.
    """

    __editor_widget: CompositeDependencyEditorWidget

    def __init__(self, item: CompositeDependency, fomod_path: Optional[Path]) -> None:
        super().__init__(item, fomod_path, show_title=True)

        self.__editor_widget.changed.connect(self.changed.emit)

    @override
    @classmethod
    def get_display_name(cls) -> str:
        return QApplication.translate(
            "DependencyEditorTab", "Edit module dependencies..."
        )

    @override
    @classmethod
    def get_title(cls) -> str:
        return QApplication.translate("DependencyEditorTab", "Module Dependencies")

    @override
    @classmethod
    def get_description(cls) -> str:
        return QApplication.translate(
            "DependencyEditorTab",
            "These are the dependencies the mod depends on. It is up to the mod manager "
            "whether this is considered or not.",
        )

    @override
    def _init_ui(self) -> None:
        super()._init_ui()

        self.__editor_widget = CompositeDependencyEditorWidget(self._item)
        self._vlayout.addWidget(self.__editor_widget)

    @override
    def validate(self) -> None:
        try:
            self.__editor_widget.validate()
        except EmptyError:
            pass

    @override
    def save(self) -> CompositeDependency:
        self._item = self.__editor_widget.save()

        self.saved.emit(self._item)
        return self._item
