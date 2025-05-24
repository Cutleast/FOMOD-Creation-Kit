"""
Copyright (c) Cutleast
"""

from typing import override

from PySide6.QtWidgets import QApplication

from core.fomod.module_config.file_list import FileList

from .base_editor_widget import BaseEditorWidget


class RequiredFilesEditorWidget(BaseEditorWidget[FileList]):
    """
    Widget class for editing the required install files of a FOMOD installer.
    """

    @override
    @classmethod
    def get_display_name(cls) -> str:
        return QApplication.translate(
            "RequiredFilesEditorWidget", "Edit required file installs..."
        )

    @override
    def validate(self) -> None: ...

    @override
    def save(self) -> FileList:
        self.saved.emit(self._item)
        return self._item
