"""
Copyright (c) Cutleast
"""

from typing import override

from PySide6.QtWidgets import QApplication

from core.fomod.module_config.module_config import ConditionalFileInstallList
from core.fomod_editor.exceptions import EmptyError

from .base_editor_widget import BaseEditorWidget
from .condition_editor.install_pattern_list_editor_widget import (
    InstallPatternListEditorWidget,
)


class ConditionalFilesEditorTab(BaseEditorWidget[ConditionalFileInstallList]):
    """
    Widget class for editing the conditional install files of a FOMOD installer.
    """

    __editor_widget: InstallPatternListEditorWidget

    @override
    def _post_init(self) -> None:
        self.__editor_widget.changed.connect(self.changed.emit)

    @override
    @classmethod
    def get_display_name(cls) -> str:
        return QApplication.translate(
            "ConditionalFilesEditorTab", "Edit conditional files..."
        )

    @override
    @classmethod
    def get_title(cls) -> str:
        return QApplication.translate(
            "ConditionalFilesEditorTab", "Conditional files to install"
        )

    @override
    def _init_ui(self) -> None:
        super()._init_ui()

        self.__editor_widget = InstallPatternListEditorWidget(
            self._item.patterns, self._fomod_path
        )
        self._vlayout.addWidget(self.__editor_widget)

    @override
    def validate(self) -> None:
        try:
            self.__editor_widget.validate()
        except EmptyError:
            pass

    @override
    def save(self) -> ConditionalFileInstallList:
        self._item.patterns = self.__editor_widget.save()

        self.saved.emit(self._item)
        return self._item
