"""
Copyright (c) Cutleast
"""

from pathlib import Path
from typing import Optional, Sequence, override

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QSplitter

from core.fomod.module_config.install_step.install_step import InstallStep
from core.fomod.module_config.install_step.order import Order
from core.fomod.module_config.install_step.step_list import StepList
from core.fomod_editor.exceptions import EmptyError
from ui.widgets.tree_widget_editor import TreeWidgetEditor

from ..base_editor_widget import BaseEditorWidget
from ..editor_dialog import EditorDialog
from .install_step_editor_widget import InstallStepEditorWidget
from .install_step_preview_widget import InstallStepPreviewWidget


class StepListEditorWidget(BaseEditorWidget[StepList]):
    """
    Widget for editing a list of install steps.
    """

    class StepsTreeWidget(TreeWidgetEditor[InstallStep]):
        """
        Adapted tree editor widget for install steps (has drag'n drop reordering and
        single selection mode).
        """

        def __init__(self, initial_items: Sequence[InstallStep] = []) -> None:
            super().__init__(initial_items)

            self.changed.connect(
                lambda: self._remove_action.setEnabled(len(self.getItems()) > 1)
            )
            self._remove_action.setEnabled(len(self.getItems()) > 1)

        @override
        def _on_selection_change(self) -> None:
            super()._on_selection_change()

            self._remove_action.setEnabled(
                len(self._tree_widget.selectedItems()) > 0 and len(self.getItems()) > 1
            )

    __splitter: QSplitter
    __steps_tree_widget: StepsTreeWidget
    __install_step_preview_widget: InstallStepPreviewWidget

    def __init__(self, item: StepList, fomod_path: Optional[Path] = None) -> None:
        super().__init__(item, fomod_path)

        self.__steps_tree_widget.changed.connect(self.changed.emit)
        self.__steps_tree_widget.currentItemChanged.connect(
            self.__install_step_preview_widget.set_item
        )
        self.__steps_tree_widget.onAdd.connect(self.__add_install_step)
        self.__steps_tree_widget.onEdit.connect(self.__edit_install_step)
        self.__install_step_preview_widget.onEdit.connect(self.__edit_install_step)

        if item.install_steps:
            self.__steps_tree_widget.setCurrentItem(item.install_steps[0])

    @override
    @classmethod
    def get_display_name(cls) -> str:
        return QApplication.translate("StepListEditorWidget", "Edit install steps...")

    @override
    def _init_ui(self) -> None:
        super()._init_ui()

        self.__splitter = QSplitter(Qt.Orientation.Horizontal)
        self._vlayout.addWidget(self.__splitter, stretch=1)

        self.__init_steps_tree_widget()
        self.__init_install_step_preview_widget()

        # self.__splitter.setStretchFactor(0, 1)
        self.__splitter.setStretchFactor(1, 1)
        # self.__splitter.setSizes([300, self.__splitter.width() - 300])

    def __init_steps_tree_widget(self) -> None:
        self.__steps_tree_widget = StepListEditorWidget.StepsTreeWidget(
            self._item.install_steps
        )
        self.__splitter.addWidget(self.__steps_tree_widget)

    def __init_install_step_preview_widget(self) -> None:
        self.__install_step_preview_widget = InstallStepPreviewWidget(
            fomod_path=self._fomod_path
        )
        self.__splitter.addWidget(self.__install_step_preview_widget)

    def __add_install_step(self) -> None:
        item = InstallStep.create()
        dialog: EditorDialog[InstallStepEditorWidget] = EditorDialog(
            InstallStepEditorWidget(item, self._fomod_path), validate_on_init=True
        )

        if dialog.exec() == EditorDialog.DialogCode.Accepted:
            self.__steps_tree_widget.addItem(item)

    def __edit_install_step(self, item: InstallStep) -> None:
        dialog: EditorDialog[InstallStepEditorWidget] = EditorDialog(
            InstallStepEditorWidget(item, self._fomod_path)
        )

        if dialog.exec() == EditorDialog.DialogCode.Accepted:
            self.__steps_tree_widget.updateItem(item)
            self.__install_step_preview_widget.set_item(item)

    @override
    def validate(self) -> None:
        if not self.__steps_tree_widget.getItems():
            raise EmptyError

    @override
    def save(self) -> StepList:
        self._item.install_steps = self.__steps_tree_widget.getItems()
        self._item.order = Order.Explicit

        self.saved.emit(self._item)
        return self._item
