"""
Copyright (c) Cutleast
"""

from typing import override

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

    @override
    def _post_init(self) -> None:
        self.__editor_widget.changed.connect(self.changed.emit)

    @override
    @classmethod
    def get_display_name(cls) -> str:
        return QApplication.translate("DependencyEditorTab", "Edit mod requirements...")

    @override
    @classmethod
    def get_title(cls) -> str:
        return QApplication.translate("DependencyEditorTab", "Mod Requirements")

    @override
    @classmethod
    def get_description(cls) -> str:
        return QApplication.translate(
            "DependencyEditorTab",
            "These are the requirements for your mod. If your mod depends on other mods "
            "to be installed and active, you can add their file(s) as file dependencies "
            "below. If the requirements are not met, the mod will not be installed.",
        )

    @override
    def _init_ui(self) -> None:
        super()._init_ui()

        self.__editor_widget = CompositeDependencyEditorWidget(
            self._item, self._fomod_path, self._flag_names_supplier
        )
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

    @override
    def discard(self) -> None:
        self.__editor_widget.discard()
        self.discarded.emit()
