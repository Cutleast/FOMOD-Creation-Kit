"""
Copyright (c) Cutleast
"""

from pathlib import Path
from typing import Optional, override

from PySide6.QtWidgets import QApplication, QLabel

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

    def __init__(
        self, item: ConditionalFileInstallList, fomod_path: Optional[Path]
    ) -> None:
        super().__init__(item, fomod_path)

        self.__editor_widget.changed.connect(self.changed.emit)

    @override
    @classmethod
    def get_display_name(cls) -> str:
        return QApplication.translate(
            "ConditionalFilesEditorWidget", "Edit conditional files..."
        )

    @override
    def _init_ui(self) -> None:
        super()._init_ui()

        self.__init_header()
        self.__init_editor_widget()

    def __init_header(self) -> None:
        title_label = QLabel(self.tr("Conditional files to install"))
        title_label.setObjectName("h2")
        self._vlayout.addWidget(title_label)

    def __init_editor_widget(self) -> None:
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
