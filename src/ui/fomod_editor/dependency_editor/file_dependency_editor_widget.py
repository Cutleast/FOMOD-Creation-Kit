"""
Copyright (c) Cutleast
"""

from pathlib import Path
from typing import Optional, override

from PySide6.QtWidgets import QApplication, QHBoxLayout, QLabel, QLineEdit

from core.fomod.module_config.dependency.file_dependency import FileDependency
from core.fomod_editor.exceptions import FileNameIsMissingError
from ui.widgets.enum_dropdown import EnumDropdown

from ..base_editor_widget import BaseEditorWidget


class FileDependencyEditorWidget(BaseEditorWidget[FileDependency]):
    """
    Widget for editing a FileDependency.
    """

    __file_name_entry: QLineEdit
    __state_dropdown: EnumDropdown[FileDependency.State]

    def __init__(self, item: FileDependency, fomod_path: Optional[Path]) -> None:
        super().__init__(item, fomod_path)

        self.__file_name_entry.textChanged.connect(lambda _: self.changed.emit())
        self.__state_dropdown.currentValueChanged.connect(lambda _: self.changed.emit())

        self.setBaseSize(500, 150)

    @override
    def _init_ui(self) -> None:
        super()._init_ui()

        help_label = QLabel(
            self.tr("A file the dependency depends on to be fulfilled.")
        )
        self._vlayout.addWidget(help_label)

        self.__file_name_entry = QLineEdit()
        self.__file_name_entry.setPlaceholderText(
            self.tr('File name, eg. "skse_loader64.exe"')
        )
        self.__file_name_entry.setText(self._item.file)
        self._vlayout.addWidget(self.__file_name_entry)

        hlayout = QHBoxLayout()
        self._vlayout.addLayout(hlayout)

        hlayout.addWidget(QLabel(self.tr("State:")))

        self.__state_dropdown = EnumDropdown(
            enum_type=FileDependency.State,
            initial_value=self._item.state,
        )
        hlayout.addWidget(self.__state_dropdown)

    @override
    @classmethod
    def get_display_name(cls) -> str:
        return QApplication.translate(
            "FileDependencyEditorWidget", "Edit file dependency..."
        )

    @override
    def validate(self) -> None:
        if not self.__file_name_entry.text().strip():
            raise FileNameIsMissingError

        self.__state_dropdown.getCurrentValue()

    @override
    def save(self) -> FileDependency:
        self._item.file = self.__file_name_entry.text().strip()
        self._item.state = self.__state_dropdown.getCurrentValue()

        self.saved.emit(self._item)
        return self._item
