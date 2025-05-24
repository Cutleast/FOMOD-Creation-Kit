"""
Copyright (c) Cutleast
"""

from typing import override

from PySide6.QtWidgets import QApplication, QLabel, QLineEdit

from core.fomod.module_config.dependency.flag_dependency import FlagDependency
from core.fomod_editor.exceptions import NameIsMissingError, ValueIsMissingError
from ui.fomod_editor.base_editor_widget import BaseEditorWidget


class FlagDependencyEditorWidget(BaseEditorWidget[FlagDependency]):
    """
    Widget for editing a FlagDependency.
    """

    __name_entry: QLineEdit
    __value_entry: QLineEdit

    def __init__(self, item: FlagDependency) -> None:
        super().__init__(item)

        self.__name_entry.textChanged.connect(lambda _: self.changed.emit())
        self.__value_entry.textChanged.connect(lambda _: self.changed.emit())

        self.resize(800, 250)

    @override
    def _init_ui(self) -> None:
        super()._init_ui()

        help_label = QLabel(
            self.tr("A flag the dependency depends on to be fulfilled.")
        )
        self._vlayout.addWidget(help_label)

        self.__name_entry = QLineEdit()
        self.__name_entry.setPlaceholderText(self.tr('Name of the flag, eg. "test"'))
        self.__name_entry.setText(self._item.flag)
        self._vlayout.addWidget(self.__name_entry)

        self.__value_entry = QLineEdit()
        self.__value_entry.setPlaceholderText(
            self.tr('Value of the flag, eg. "true" or "on"')
        )
        self.__value_entry.setText(self._item.value)
        self._vlayout.addWidget(self.__value_entry)

    @override
    @classmethod
    def get_display_name(cls) -> str:
        return QApplication.translate(
            "FlagDependencyEditorWidget", "Edit flag dependency..."
        )

    @override
    def validate(self) -> None:
        if not self.__name_entry.text().strip():
            raise NameIsMissingError

        if not self.__value_entry.text().strip():
            raise ValueIsMissingError

    @override
    def save(self) -> FlagDependency:
        self._item.flag = self.__name_entry.text().strip()
        self._item.value = self.__value_entry.text().strip()

        self.saved.emit(self._item)
        return self._item
