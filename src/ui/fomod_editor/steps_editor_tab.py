"""
Copyright (c) Cutleast
"""

from pathlib import Path
from typing import Optional, override

from PySide6.QtWidgets import QApplication, QLabel

from core.fomod.module_config.install_step.step_list import StepList

from .base_editor_widget import BaseEditorWidget
from .install_step_editor.step_list_editor_widget import StepListEditorWidget


class StepsEditorTab(BaseEditorWidget[StepList]):
    """
    Widget class for editing the install steps (pages) of a FOMOD installer.
    """

    __editor_widget: StepListEditorWidget

    def __init__(self, item: StepList, fomod_path: Optional[Path] = None) -> None:
        super().__init__(item, fomod_path)

        self.__editor_widget.changed.connect(self.changed.emit)

    @override
    @classmethod
    def get_display_name(cls) -> str:
        return QApplication.translate("StepsEditorWidget", "Edit installation steps...")

    @override
    def _init_ui(self) -> None:
        super()._init_ui()

        self.__init_header()
        self.__init_editor_widget()

    def __init_header(self) -> None:
        title_label = QLabel(self.tr("Installation steps"))
        title_label.setObjectName("h2")
        self._vlayout.addWidget(title_label)

        help_label = QLabel(
            self.tr("These are the installation steps (or pages) of a FOMOD installer.")
        )
        self._vlayout.addWidget(help_label)

    def __init_editor_widget(self) -> None:
        self.__editor_widget = StepListEditorWidget(self._item, self._fomod_path)
        self._vlayout.addWidget(self.__editor_widget)

    @override
    def validate(self) -> None:
        self.__editor_widget.validate()

    @override
    def save(self) -> StepList:
        self._item = self.__editor_widget.save()

        self.saved.emit(self._item)
        return self._item
