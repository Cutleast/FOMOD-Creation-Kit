"""
Copyright (c) Cutleast
"""

from pathlib import Path
from typing import override

from PySide6.QtGui import Qt
from PySide6.QtWidgets import QApplication, QLabel, QStackedWidget, QVBoxLayout, QWidget

from core.fomod.module_config.plugin.plugin_type import PluginType
from core.fomod.module_config.plugin.plugin_type_descriptor import (
    DependencyPluginType,
    PluginTypeDescriptor,
)
from core.utilities.localized_enum import LocalizedEnum
from ui.widgets.enum_dropdown import EnumDropdown
from ui.widgets.enum_radiobutton_widget import EnumRadiobuttonsWidget

from ..base_editor_widget import BaseEditorWidget
from .dependency_plugin_type_editor_widget import DependencyPluginTypeEditorWidget


class TypeDescriptorEditorWidget(BaseEditorWidget[PluginTypeDescriptor]):
    """
    Widget for editing a plugin type descriptor.
    """

    class DescriptorType(LocalizedEnum):
        """Enum for the selectable types of plugin type descriptors."""

        Static = "Static"
        """Indicating a static plugin type."""

        Dynamic = "Dynamic"
        """Indicating a dynamic plugin type depending on some dependency patterns."""

        @override
        def get_localized_name(self) -> str:
            locs: dict[TypeDescriptorEditorWidget.DescriptorType, str] = {
                TypeDescriptorEditorWidget.DescriptorType.Static: QApplication.translate(
                    "TypeDescriptorEditorWidget", "Static Type"
                ),
                TypeDescriptorEditorWidget.DescriptorType.Dynamic: QApplication.translate(
                    "TypeDescriptorEditorWidget", "Dynamic Type"
                ),
            }

            return locs[self]

        @override
        def get_localized_description(self) -> str:
            locs: dict[TypeDescriptorEditorWidget.DescriptorType, str] = {
                TypeDescriptorEditorWidget.DescriptorType.Static: QApplication.translate(
                    "TypeDescriptorEditorWidget", "The type of the plugin is static."
                ),
                TypeDescriptorEditorWidget.DescriptorType.Dynamic: QApplication.translate(
                    "TypeDescriptorEditorWidget",
                    "The type of the plugin depends on some dependency patterns..",
                ),
            }

            return locs[self]

    __descriptor_type_selector: EnumRadiobuttonsWidget[DescriptorType]
    __stack_widget: QStackedWidget
    __static_type_selector: EnumDropdown[PluginType.Type]
    __dynamic_type_editor: DependencyPluginTypeEditorWidget

    def __init__(
        self, item: PluginTypeDescriptor, fomod_path: Path | None = None
    ) -> None:
        super().__init__(item, fomod_path)

        self.__descriptor_type_selector.currentValueChanged.connect(
            self.__on_type_changed
        )
        self.__static_type_selector.currentValueChanged.connect(
            lambda _: self.changed.emit()
        )
        self.__dynamic_type_editor.changed.connect(self.changed.emit)

    @override
    @classmethod
    def get_display_name(cls) -> str:
        return QApplication.translate(
            "TypeDescriptorEditorWidget", "Edit plugin type descriptor..."
        )

    @override
    @classmethod
    def get_description(cls) -> str:
        return QApplication.translate(
            "TypeDescriptorEditorWidget",
            "The type of a plugin determines its pre-selection state.",
        )

    @override
    def _init_ui(self) -> None:
        super()._init_ui()

        self.__init_descriptor_type_selector()
        self.__init_stack_widget()
        self.__init_static_type_selector()
        self.__init_dynamic_type_editor()

        if (
            self.__descriptor_type_selector.getCurrentValue()
            == TypeDescriptorEditorWidget.DescriptorType.Static
        ):
            self.__stack_widget.setCurrentIndex(0)
        else:
            self.__stack_widget.setCurrentIndex(1)

    def __init_descriptor_type_selector(self) -> None:
        self.__descriptor_type_selector = EnumRadiobuttonsWidget(
            enum_type=TypeDescriptorEditorWidget.DescriptorType,
            initial_value=(
                TypeDescriptorEditorWidget.DescriptorType.Static
                if self._item.dependency_type is None
                else TypeDescriptorEditorWidget.DescriptorType.Dynamic
            ),
            orientation=Qt.Orientation.Horizontal,
        )
        self._vlayout.addWidget(
            self.__descriptor_type_selector, alignment=Qt.AlignmentFlag.AlignHCenter
        )

    def __init_stack_widget(self) -> None:
        self.__stack_widget = QStackedWidget()
        self._vlayout.addWidget(self.__stack_widget)

    def __init_static_type_selector(self) -> None:
        # a separate widget is required here to prevent the dropdown from expanding to
        # the bottom
        widget = QWidget()
        self.__stack_widget.addWidget(widget)

        vlayout = QVBoxLayout()
        vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        vlayout.setContentsMargins(0, 0, 0, 0)
        widget.setLayout(vlayout)

        self.__static_type_selector = EnumDropdown(
            enum_type=PluginType.Type,
            initial_value=self._item.type.name if self._item.type is not None else None,
        )
        vlayout.addWidget(self.__static_type_selector)

        help_label = QLabel(PluginType.Type.get_localized_summary())
        help_label.setWordWrap(True)
        vlayout.addWidget(help_label)

    def __init_dynamic_type_editor(self) -> None:
        self.__dynamic_type_editor = DependencyPluginTypeEditorWidget(
            self._item.dependency_type or DependencyPluginType.create(),
            self._fomod_path,
        )
        self.__stack_widget.addWidget(self.__dynamic_type_editor)

    def __on_type_changed(self, value: DescriptorType) -> None:
        if value == TypeDescriptorEditorWidget.DescriptorType.Static:
            self.__stack_widget.setCurrentIndex(0)
        else:
            self.__stack_widget.setCurrentIndex(1)

        self.changed.emit()

    @override
    def validate(self) -> None:
        if (
            self.__descriptor_type_selector.getCurrentValue()
            == TypeDescriptorEditorWidget.DescriptorType.Dynamic
        ):
            self.__dynamic_type_editor.validate()

    @override
    def save(self) -> PluginTypeDescriptor:
        if (
            self.__descriptor_type_selector.getCurrentValue()
            == TypeDescriptorEditorWidget.DescriptorType.Static
        ):
            self._item.dependency_type = None
            self._item.type = PluginType(
                name=self.__static_type_selector.getCurrentValue()
            )
        else:
            self._item.dependency_type = self.__dynamic_type_editor.save()
            self._item.type = None

        self.saved.emit(self._item)
        return self._item
