"""
Copyright (c) Cutleast
"""

from typing import override

from PySide6.QtWidgets import QApplication, QLabel

from core.fomod.module_config.file_list import FileList
from core.fomod_editor.exceptions import EmptyError

from .base_editor_widget import BaseEditorWidget
from .file_list_editor_widget import FileListEditorWidget


class RequiredFilesEditorTab(BaseEditorWidget[FileList]):
    """
    Widget class for editing the required install files of a FOMOD installer.
    """

    __file_list_editor_widget: FileListEditorWidget

    def __init__(self, item: FileList) -> None:
        super().__init__(item)

        self.__file_list_editor_widget.changed.connect(self.changed.emit)

    @override
    @classmethod
    def get_display_name(cls) -> str:
        return QApplication.translate(
            "RequiredFilesEditorWidget", "Edit required file installs..."
        )

    @override
    def _init_ui(self) -> None:
        super()._init_ui()

        self._vlayout.setContentsMargins(0, 0, 0, 0)

        self.__init_header()
        self.__init_editor_widget()

    def __init_header(self) -> None:
        title_label = QLabel(self.tr("Required files to install"))
        title_label.setObjectName("h2")
        self._vlayout.addWidget(title_label)

        help_label = QLabel(
            self.tr(
                "This list defines which files and folders must be installed by the "
                "installer."
            )
        )
        self._vlayout.addWidget(help_label)

    def __init_editor_widget(self) -> None:
        self.__file_list_editor_widget = FileListEditorWidget(self._item)
        self.__file_list_editor_widget.setContentsMargins(0, 0, 0, 0)
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
