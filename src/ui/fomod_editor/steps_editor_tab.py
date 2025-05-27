"""
Copyright (c) Cutleast
"""

from typing import override

from PySide6.QtWidgets import QApplication

from core.fomod.module_config.install_step.step_list import StepList

from .base_editor_widget import BaseEditorWidget


class StepsEditorTab(BaseEditorWidget[StepList]):
    """
    Widget class for editing the install steps (pages) of a FOMOD installer.
    """

    @override
    @classmethod
    def get_display_name(cls) -> str:
        return QApplication.translate("StepsEditorWidget", "Edit installation steps...")

    @override
    def validate(self) -> None: ...

    @override
    def save(self) -> StepList:
        self.saved.emit(self._item)
        return self._item
