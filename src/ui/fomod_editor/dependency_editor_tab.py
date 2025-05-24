"""
Copyright (c) Cutleast
"""

from typing import override

from PySide6.QtWidgets import QApplication, QLabel

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

    def __init__(self, item: CompositeDependency) -> None:
        super().__init__(item)

        self.__editor_widget.changed.connect(self.changed.emit)

    @override
    @classmethod
    def get_display_name(cls) -> str:
        return QApplication.translate(
            "DependencyEditorWidget", "Edit module dependencies..."
        )

    @override
    def _init_ui(self) -> None:
        super()._init_ui()

        self._vlayout.setContentsMargins(0, 0, 0, 0)

        self.__init_header()
        self.__init_editor_widget()

    def __init_header(self) -> None:
        title_label = QLabel(self.tr("Module Dependencies"))
        title_label.setObjectName("h2")
        self._vlayout.addWidget(title_label)

        help_label = QLabel(self.tr("These are the dependencies the mod depends on."))
        self._vlayout.addWidget(help_label)

    def __init_editor_widget(self) -> None:
        self.__editor_widget = CompositeDependencyEditorWidget(self._item)
        self.__editor_widget.setContentsMargins(0, 0, 0, 0)
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
