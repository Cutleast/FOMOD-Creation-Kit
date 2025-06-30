"""
Copyright (c) Cutleast
"""

from typing import override

from PySide6.QtWidgets import QApplication, QLineEdit

from core.fomod.module_config.condition.set_condition_flag import SetConditionFlag
from core.fomod_editor.exceptions import NameIsMissingError, ValueIsMissingError
from ui.widgets.auto_complete_combobox import AutoCompleteCombobox

from ..base_editor_widget import BaseEditorWidget


class SetConditionFlagEditorWidget(BaseEditorWidget[SetConditionFlag]):
    """
    Widget for editing a SetConditionFlag.
    """

    __name_entry: AutoCompleteCombobox
    __value_entry: QLineEdit

    @override
    def _post_init(self) -> None:
        self.__name_entry.currentTextChanged.connect(lambda _: self.changed.emit())
        self.__value_entry.textChanged.connect(lambda _: self.changed.emit())

    @override
    @classmethod
    def get_display_name(cls) -> str:
        return QApplication.translate(
            "SetConditionFlagEditorWidget", "Edit set condition flag..."
        )

    @override
    @classmethod
    def get_description(cls) -> str:
        return QApplication.translate(
            "SetConditionFlagEditorWidget",
            "A flag to be set to a specific value when the plugin is selected.",
        )

    @override
    def _init_ui(self) -> None:
        super()._init_ui()

        self.__name_entry = AutoCompleteCombobox()
        self.__name_entry.setPlaceholderText(self.tr('Name of the flag, eg. "test"'))
        self.__name_entry.addItems(self._flag_names_supplier())
        self.__name_entry.setCurrentText(self._item.name)
        self._vlayout.addWidget(self.__name_entry)

        self.__value_entry = QLineEdit()
        self.__value_entry.setPlaceholderText(
            self.tr('Value of the flag, eg. "true" or "on"')
        )
        self.__value_entry.setText(self._item.value)
        self._vlayout.addWidget(self.__value_entry)

        self.setBaseSize(500, 140)

    @override
    def validate(self) -> None:
        if not self.__name_entry.currentText().strip():
            raise NameIsMissingError

        if not self.__value_entry.text().strip():
            raise ValueIsMissingError

    @override
    def save(self) -> SetConditionFlag:
        self._item.name = self.__name_entry.currentText().strip()
        self._item.value = self.__value_entry.text().strip()

        self.saved.emit(self._item)
        return self._item
