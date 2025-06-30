"""
Copyright (c) Cutleast
"""

from typing import override

from PySide6.QtWidgets import QApplication

from core.fomod.module_config.install_step.step_list import StepList

from .base_editor_widget import BaseEditorWidget
from .install_step_editor.step_list_editor_widget import StepListEditorWidget


class StepsEditorTab(BaseEditorWidget[StepList]):
    """
    Widget class for editing the install steps (pages) of a FOMOD installer.
    """

    __editor_widget: StepListEditorWidget

    @override
    def _post_init(self) -> None:
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

        self.__editor_widget = StepListEditorWidget(
            self._item, self._fomod_path, self._flag_names_supplier
        )
        self._vlayout.addWidget(self.__editor_widget)

    @override
    def validate(self) -> None:
        self.__editor_widget.validate()

    @override
    def save(self) -> StepList:
        self._item = self.__editor_widget.save()

        self.saved.emit(self._item)
        return self._item
