"""
Copyright (c) Cutleast
"""

from typing import override

from PySide6.QtWidgets import QApplication, QHBoxLayout, QLabel, QLineEdit

from core.fomod.module_config.install_step.group import Group
from core.fomod_editor.exceptions import NameIsMissingError
from ui.widgets.enum_dropdown import EnumDropdown
from ui.widgets.help_label import HelpLabel

from ..base_editor_widget import BaseEditorWidget


class GroupEditorWidget(BaseEditorWidget[Group]):
    """
    A widget for editing the name and type of a group.
    """

    __name_entry: QLineEdit
    __type_dropdown: EnumDropdown[Group.Type]

    @override
    def _post_init(self) -> None:
        self.__name_entry.textChanged.connect(lambda _: self.changed.emit())
        self.__type_dropdown.currentValueChanged.connect(lambda _: self.changed.emit())

    @override
    @classmethod
    def get_display_name(cls) -> str:
        return QApplication.translate("GroupEditorWidget", "Edit group...")

    @override
    def _init_ui(self) -> None:
        super()._init_ui()

        self.__name_entry = QLineEdit(self._item.name)
        self.__name_entry.setPlaceholderText(
            self.tr('Name of the group, for eg. "Patches"')
        )
        self._vlayout.addWidget(self.__name_entry)

        hlayout = QHBoxLayout()
        self._vlayout.addLayout(hlayout)

        hlayout.addWidget(QLabel(self.tr("Type:")))

        self.__type_dropdown = EnumDropdown(
            enum_type=Group.Type, initial_value=self._item.type
        )
        hlayout.addWidget(self.__type_dropdown, stretch=1)

        hlayout.addWidget(
            HelpLabel(
                self.tr(
                    "The type of a group specifies if and how many plugins in the group "
                    "must be selected by the user to be able to continue."
                )
                + "\n\n"
                + Group.Type.get_localized_summary()
            )
        )

        self.setBaseSize(500, 100)

    @override
    def validate(self) -> None:
        if not self.__name_entry.text().strip():
            raise NameIsMissingError

    @override
    def save(self) -> Group:
        self._item.name = self.__name_entry.text().strip()
        self._item.type = self.__type_dropdown.getCurrentValue()

        self.saved.emit(self._item)
        return self._item
