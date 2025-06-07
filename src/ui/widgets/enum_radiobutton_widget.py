"""
Copyright (c) Cutleast
"""

from enum import Enum
from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QHBoxLayout, QRadioButton, QVBoxLayout, QWidget

from core.utilities.localized_enum import LocalizedEnum


class EnumRadiobuttonsWidget[E: Enum](QWidget):
    """
    A widget with radio buttons for selecting an enum value.
    """

    currentValueChanged = Signal(Enum)
    """
    This signal gets emitted when the selected enum value changes.

    Args:
        E: The selected enum value
    """

    __enum_type: type[E]

    __layout: QVBoxLayout | QHBoxLayout
    __enum_items: dict[E, QRadioButton]

    def __init__(
        self,
        enum_type: type[E],
        initial_value: Optional[E] = None,
        orientation: Qt.Orientation = Qt.Orientation.Vertical,
    ) -> None:
        """
        Args:
            enum_type (type[E]): Type of the enum
            initial_value (Optional[E], optional):
                Initial enum member to select. Defaults to None.
            orientation (Qt.Orientation, optional):
                Layout orientation. Defaults to Qt.Orientation.Vertical.
        """

        super().__init__()

        self.__enum_type = enum_type

        self.__init_ui(orientation)

        if initial_value is not None:
            self.__enum_items[initial_value].setChecked(True)

        for radiobutton in self.__enum_items.values():
            radiobutton.toggled.connect(
                lambda _: self.currentValueChanged.emit(self.getCurrentValue())
            )

    def __init_ui(self, orientation: Qt.Orientation) -> None:
        if orientation == Qt.Orientation.Horizontal:
            self.__layout = QHBoxLayout()
        else:
            self.__layout = QVBoxLayout()

        self.__layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.__layout)

        self.__init_radiobuttons()

    def __init_radiobuttons(self) -> None:
        self.__enum_items = {}

        if issubclass(self.__enum_type, LocalizedEnum):
            for enum_value in self.__enum_type:
                radio_button = QRadioButton(enum_value.get_localized_name())
                radio_button.setToolTip(enum_value.get_localized_description())
                self.__enum_items[enum_value] = radio_button
                self.__layout.addWidget(radio_button)
        else:
            for enum_value in self.__enum_type:
                radio_button = QRadioButton(enum_value.name)
                radio_button.setToolTip(enum_value.__doc__ or "")
                self.__enum_items[enum_value] = radio_button
                self.__layout.addWidget(radio_button)

    def getCurrentValue(self) -> E:
        """
        Returns:
            E: The currently selected enum member
        """

        for enum_value, radiobutton in self.__enum_items.items():
            if radiobutton.isChecked():
                return enum_value

        raise ValueError("No radio button is checked")

    def setCurrentValue(self, enum_value: E) -> None:
        """
        Sets the specified enum value as the currently selected.

        Args:
            enum_value (E): Enum value to select
        """

        self.__enum_items[enum_value].setChecked(True)
