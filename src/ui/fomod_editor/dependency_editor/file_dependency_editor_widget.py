"""
Copyright (c) Cutleast
"""

from typing import override

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QHBoxLayout, QLabel, QLineEdit, QVBoxLayout

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

    @override
    def _post_init(self) -> None:
        self.__file_name_entry.textChanged.connect(lambda _: self.changed.emit())
        self.__state_dropdown.currentValueChanged.connect(lambda _: self.changed.emit())

    @override
    @classmethod
    def get_display_name(cls) -> str:
        return QApplication.translate(
            "FileDependencyEditorWidget", "Edit file dependency..."
        )

    @override
    @classmethod
    def get_description(cls) -> str:
        return QApplication.translate(
            "FileDependencyEditorWidget",
            "A file dependency is the combination of a file name and a state that have "
            "to match for this dependency to be fulfilled.",
        )

    @override
    def _init_ui(self) -> None:
        super()._init_ui()

        self.__file_name_entry = QLineEdit()
        self.__file_name_entry.setPlaceholderText(
            self.tr('File name, eg. "skse_loader64.exe"')
        )
        self.__file_name_entry.setText(self._item.file)
        self._vlayout.addWidget(self.__file_name_entry)

        self._vlayout.addSpacing(10)

        hlayout = QHBoxLayout()
        self._vlayout.addLayout(hlayout)

        hlayout.addWidget(
            QLabel(self.tr("State:")), alignment=Qt.AlignmentFlag.AlignTop
        )
        hlayout.addSpacing(25)

        vlayout = QVBoxLayout()
        vlayout.setContentsMargins(0, 0, 0, 0)
        vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        hlayout.addLayout(vlayout, stretch=1)

        self.__state_dropdown = EnumDropdown(
            enum_type=FileDependency.State,
            initial_value=self._item.state,
        )
        vlayout.addWidget(self.__state_dropdown)

        state_help_label = QLabel(FileDependency.State.get_localized_summary())
        vlayout.addWidget(state_help_label)

        self.setBaseSize(500, 210)

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
