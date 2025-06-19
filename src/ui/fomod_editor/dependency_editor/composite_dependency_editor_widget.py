"""
Copyright (c) Cutleast
"""

from pathlib import Path
from typing import Optional, override

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QHBoxLayout, QLabel

from core.fomod.module_config.dependency.composite_dependency import (
    CompositeDependency,
)
from ui.widgets.enum_radiobutton_widget import EnumRadiobuttonsWidget

from ..base_editor_widget import BaseEditorWidget
from .dependency_group_editor_widget import DependencyGroupEditorWidget


class CompositeDependencyEditorWidget(BaseEditorWidget[CompositeDependency]):
    """
    Widget class for editing composite dependencies of a FOMOD installer.
    """

    __dependency_group_editor_widget: DependencyGroupEditorWidget
    __operator_selector: EnumRadiobuttonsWidget[CompositeDependency.Operator]

    def __init__(
        self,
        item: CompositeDependency,
        fomod_path: Optional[Path] = None,
        show_title: bool = False,
        show_description: bool = True,
        scrollable: bool = True,
    ) -> None:
        super().__init__(item, fomod_path, show_title, show_description, scrollable)

        self.__operator_selector.currentValueChanged.connect(
            lambda value: self.changed.emit()
        )
        self.__dependency_group_editor_widget.changed.connect(self.changed.emit)

    @override
    @classmethod
    def get_display_name(cls) -> str:
        return QApplication.translate(
            "CompositeDependencyEditorWidget", "Edit composite dependency..."
        )

    @override
    @classmethod
    def get_description(cls) -> str:
        return QApplication.translate(
            "CompositeDependencyEditorWidget",
            "Composite dependencies are used to group multiple dependencies together.",
        )

    @override
    def _init_ui(self) -> None:
        super()._init_ui()

        self.__init_operator_selector()
        self.__init_dependency_group_editor_widget()

        self.setBaseSize(700, 400)

    def __init_operator_selector(self) -> None:
        hlayout = QHBoxLayout()
        self._vlayout.addLayout(hlayout)

        hlayout.addWidget(QLabel(self.tr("Operator:")))

        self.__operator_selector = EnumRadiobuttonsWidget(
            enum_type=CompositeDependency.Operator,
            initial_value=self._item.operator,
            orientation=Qt.Orientation.Horizontal,
        )
        hlayout.addWidget(self.__operator_selector)

        hlayout.addStretch()

    def __init_dependency_group_editor_widget(self) -> None:
        self.__dependency_group_editor_widget = DependencyGroupEditorWidget(
            self._item, self._fomod_path
        )
        self._vlayout.addWidget(self.__dependency_group_editor_widget)

    @override
    def validate(self) -> None:
        self.__operator_selector.getCurrentValue()
        self.__dependency_group_editor_widget.validate()

    @override
    def save(self) -> CompositeDependency:
        self._item = self.__dependency_group_editor_widget.save()
        self._item.operator = self.__operator_selector.getCurrentValue()

        self.saved.emit(self._item)
        return self._item
