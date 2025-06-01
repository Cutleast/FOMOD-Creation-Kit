"""
Copyright (c) Cutleast
"""

from pathlib import Path
from typing import Optional, override

from PySide6.QtWidgets import QApplication, QLabel, QLineEdit

from core.fomod.module_config.condition.set_condition_flag import SetConditionFlag
from core.fomod_editor.exceptions import NameIsMissingError, ValueIsMissingError
from ui.fomod_editor.base_editor_widget import BaseEditorWidget


class SetConditionFlagEditorWidget(BaseEditorWidget[SetConditionFlag]):
    """
    Widget for editing a SetConditionFlag.
    """

    __name_entry: QLineEdit
    __value_entry: QLineEdit

    def __init__(self, item: SetConditionFlag, fomod_path: Optional[Path]) -> None:
        super().__init__(item, fomod_path)

        self.__name_entry.textChanged.connect(lambda _: self.changed.emit())
        self.__value_entry.textChanged.connect(lambda _: self.changed.emit())

        self.resize(800, 250)

    @override
    def _init_ui(self) -> None:
        super()._init_ui()

        help_label = QLabel(self.tr("A flag to be set when the plugin is selected."))
        self._vlayout.addWidget(help_label)

        self.__name_entry = QLineEdit()
        self.__name_entry.setPlaceholderText(self.tr('Name of the flag, eg. "test"'))
        self.__name_entry.setText(self._item.name)
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
            "SetConditionFlagEditorWidget", "Edit set condition flag..."
        )

    @override
    def validate(self) -> None:
        if not self.__name_entry.text().strip():
            raise NameIsMissingError

        if not self.__value_entry.text().strip():
            raise ValueIsMissingError

    @override
    def save(self) -> SetConditionFlag:
        self._item.name = self.__name_entry.text().strip()
        self._item.value = self.__value_entry.text().strip()

        self.saved.emit(self._item)
        return self._item
