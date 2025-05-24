"""
Copyright (c) Cutleast
"""

from typing import override

from PySide6.QtWidgets import QApplication

from core.fomod.module_config.module_config import ConditionalFileInstallList

from .base_editor_widget import BaseEditorWidget


class ConditionalFilesEditorTab(BaseEditorWidget[ConditionalFileInstallList]):
    """
    Widget class for editing the conditional install files of a FOMOD installer.
    """

    @override
    @classmethod
    def get_display_name(cls) -> str:
        return QApplication.translate(
            "ConditionalFilesEditorWidget", "Edit conditional files..."
        )

    @override
    def validate(self) -> None: ...

    @override
    def save(self) -> ConditionalFileInstallList:
        self.saved.emit(self._item)
        return self._item
