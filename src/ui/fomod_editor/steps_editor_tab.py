"""
Copyright (c) Cutleast
"""

from pathlib import Path
from typing import Optional, override

from PySide6.QtWidgets import QApplication

from core.fomod.module_config.install_step.step_list import StepList

from .base_editor_widget import BaseEditorWidget
from .install_step_editor.step_list_editor_widget import StepListEditorWidget


class StepsEditorTab(BaseEditorWidget[StepList]):
    """
    Widget class for editing the install steps (pages) of a FOMOD installer.
    """

    __editor_widget: StepListEditorWidget

    def __init__(self, item: StepList, fomod_path: Optional[Path] = None) -> None:
        super().__init__(item, fomod_path, show_title=True)

        self.__editor_widget.changed.connect(self.changed.emit)

    @override
    @classmethod
    def get_display_name(cls) -> str:
        return QApplication.translate("StepsEditorTab", "Edit installation steps...")

    @override
    @classmethod
    def get_title(cls) -> str:
        return QApplication.translate("StepsEditorTab", "Installation steps")

    @override
    @classmethod
    def get_description(cls) -> str:
        return QApplication.translate(
            "StepsEditorTab",
            "These are the installation steps (or pages) of a FOMOD installer.",
        )

    @override
    def _init_ui(self) -> None:
        super()._init_ui()

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
