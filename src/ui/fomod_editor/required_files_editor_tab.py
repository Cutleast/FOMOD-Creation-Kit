"""
Copyright (c) Cutleast
"""

from typing import override

from PySide6.QtWidgets import QApplication

from core.fomod.module_config.file_list import FileList
from core.fomod_editor.exceptions import EmptyError

from .base_editor_widget import BaseEditorWidget
from .file_list_editor_widget import FileListEditorWidget


class RequiredFilesEditorTab(BaseEditorWidget[FileList]):
    """
    Widget class for editing the required install files of a FOMOD installer.
    """

    __file_list_editor_widget: FileListEditorWidget

    @override
    def _post_init(self) -> None:
        self.__file_list_editor_widget.changed.connect(self.changed.emit)

    @override
    @classmethod
    def get_display_name(cls) -> str:
        return QApplication.translate(
            "RequiredFilesEditorTab", "Edit required file installs..."
        )

    @override
    @classmethod
    def get_title(cls) -> str:
        return QApplication.translate(
            "RequiredFilesEditorTab", "Required files to install"
        )

    @override
    @classmethod
    def get_description(cls) -> str:
        return QApplication.translate(
            "RequiredFilesEditorTab",
            "This list defines which files and folders must be installed by the "
            "installer.",
        )

    @override
    def _init_ui(self) -> None:
        super()._init_ui()

        self.__file_list_editor_widget = FileListEditorWidget(
            self._item, self._fomod_path, show_description=False
        )
        self._vlayout.addWidget(self.__file_list_editor_widget)

    @override
    def validate(self) -> None:
        try:
            self.__file_list_editor_widget.validate()
        except EmptyError:
            pass

    @override
    def save(self) -> FileList:
        self._item = self.__file_list_editor_widget.save()

        self.saved.emit(self._item)
        return self._item
