"""
Copyright (c) Cutleast
"""

from typing import override

from PySide6.QtCore import QEvent, QObject, Qt, Signal
from PySide6.QtGui import QWheelEvent
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QLabel,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from core.config.app_config import AppConfig
from core.config.behavior_config import BehaviorConfig
from core.fomod_editor.history import History
from core.utilities.localisation import Language
from core.utilities.logger import Logger
from ui.utilities.ui_mode import UIMode
from ui.widgets.enum_dropdown import EnumDropdown
from ui.widgets.smooth_scroll_area import SmoothScrollArea


class SettingsWidget(SmoothScrollArea):
    """
    Widget for configuring application settings.
    """

    changed = Signal()
    """
    This signal gets emitted when a setting changes.
    """

    restart_required = Signal()
    """
    This signal gets emitted when a setting change requires a restart.
    """

    __app_config: AppConfig
    __behavior_config: BehaviorConfig
    __history: History

    __vlayout: QVBoxLayout

    __log_level_box: EnumDropdown[Logger.Level]
    __log_num_of_files_box: QSpinBox
    __log_visible: QCheckBox
    __language_box: EnumDropdown[Language]
    __ui_mode_box: EnumDropdown[UIMode]
    __clear_history_button: QPushButton

    __finalize_checkbox: QCheckBox
    __validate_xml_checkbox: QCheckBox
    __module_config_encoding_dropdown: EnumDropdown[BehaviorConfig.ModuleConfigEncoding]

    def __init__(
        self, app_config: AppConfig, behavior_config: BehaviorConfig, history: History
    ) -> None:
        super().__init__()

        self.__app_config = app_config
        self.__behavior_config = behavior_config
        self.__history = history

        self.__init_ui()

    def __init_ui(self) -> None:
        scroll_widget = QWidget()
        scroll_widget.setObjectName("transparent")
        self.setWidget(scroll_widget)

        self.__vlayout = QVBoxLayout()
        self.__vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll_widget.setLayout(self.__vlayout)

        self.__init_app_settings()
        self.__init_behavior_settings()

    def __init_app_settings(self) -> None:
        app_settings_group = QGroupBox(self.tr("App settings"))
        app_settings_group.setObjectName("title")
        self.__vlayout.addWidget(app_settings_group)

        app_settings_glayout = QGridLayout()
        app_settings_glayout.setContentsMargins(0, 0, 0, 0)
        app_settings_group.setLayout(app_settings_glayout)

        log_level_label = QLabel(self.tr("Log level:"))
        app_settings_glayout.addWidget(log_level_label, 0, 0)

        self.__log_level_box = EnumDropdown(Logger.Level, self.__app_config.log_level)
        self.__log_level_box.installEventFilter(self)
        self.__log_level_box.currentValueChanged.connect(lambda _: self.changed.emit())
        self.__log_level_box.currentValueChanged.connect(
            lambda _: self.restart_required.emit()
        )
        app_settings_glayout.addWidget(self.__log_level_box, 0, 1)

        log_num_of_files_label = QLabel(self.tr("Number of newest log files to keep:"))
        app_settings_glayout.addWidget(log_num_of_files_label, 1, 0)

        self.__log_num_of_files_box = QSpinBox()
        self.__log_num_of_files_box.setRange(-1, 255)
        self.__log_num_of_files_box.setValue(self.__app_config.log_num_of_files)
        self.__log_num_of_files_box.installEventFilter(self)
        self.__log_num_of_files_box.valueChanged.connect(lambda _: self.changed.emit())
        self.__log_num_of_files_box.valueChanged.connect(
            lambda _: self.restart_required.emit()
        )
        app_settings_glayout.addWidget(self.__log_num_of_files_box, 1, 1)

        self.__log_visible = QCheckBox(
            self.tr("Display log at the bottom of the main window")
        )
        self.__log_visible.setChecked(self.__app_config.log_visible)
        self.__log_visible.checkStateChanged.connect(lambda _: self.changed.emit())
        self.__log_visible.checkStateChanged.connect(
            lambda _: self.restart_required.emit()
        )
        app_settings_glayout.addWidget(self.__log_visible, 2, 0, 1, 2)

        language_label = QLabel(self.tr("Language:"))
        app_settings_glayout.addWidget(language_label, 3, 0)

        self.__language_box = EnumDropdown(Language, self.__app_config.language)
        self.__language_box.installEventFilter(self)
        self.__language_box.currentValueChanged.connect(lambda _: self.changed.emit())
        self.__language_box.currentValueChanged.connect(
            lambda _: self.restart_required.emit()
        )
        app_settings_glayout.addWidget(self.__language_box, 3, 1)

        ui_mode_label = QLabel(self.tr("UI mode:"))
        app_settings_glayout.addWidget(ui_mode_label, 4, 0)

        self.__ui_mode_box = EnumDropdown(UIMode, self.__app_config.ui_mode)
        self.__ui_mode_box.installEventFilter(self)
        self.__ui_mode_box.currentValueChanged.connect(lambda _: self.changed.emit())
        self.__ui_mode_box.currentValueChanged.connect(
            lambda _: self.restart_required.emit()
        )
        app_settings_glayout.addWidget(self.__ui_mode_box, 4, 1)

        self.__clear_history_button = QPushButton(
            self.tr("Clear history of recently opened FOMOD installers")
        )
        self.__clear_history_button.clicked.connect(self.__clear_history)
        self.__clear_history_button.setEnabled(len(self.__history.recent_fomods) > 0)
        app_settings_glayout.addWidget(self.__clear_history_button, 5, 0, 1, 2)

    def __init_behavior_settings(self) -> None:
        behavior_settings_group = QGroupBox(self.tr("Behavior settings"))
        behavior_settings_group.setObjectName("title")
        self.__vlayout.addWidget(behavior_settings_group)

        behavior_settings_flayout = QFormLayout()
        behavior_settings_group.setLayout(behavior_settings_flayout)

        self.__finalize_checkbox = QCheckBox(self.tr("Finalize on save (recommended)"))
        self.__finalize_checkbox.setToolTip(
            self.tr(
                "Finalizing means copying all files from outside of the FOMOD "
                "into the FOMOD's folder and making the paths relative.\n"
                "This makes the entire mod practically ready to be packed in a zip file "
                "and distributed."
            )
        )
        self.__finalize_checkbox.setChecked(self.__behavior_config.finalize_on_save)
        self.__finalize_checkbox.stateChanged.connect(lambda _: self.changed.emit())
        behavior_settings_flayout.addRow(self.__finalize_checkbox)

        self.__validate_xml_checkbox = QCheckBox(self.tr("Validate XML files on save"))
        self.__validate_xml_checkbox.setChecked(
            self.__behavior_config.validate_xml_on_save
        )
        self.__validate_xml_checkbox.stateChanged.connect(lambda _: self.changed.emit())
        behavior_settings_flayout.addRow(self.__validate_xml_checkbox)

        self.__module_config_encoding_dropdown = EnumDropdown(
            BehaviorConfig.ModuleConfigEncoding,
            self.__behavior_config.module_config_encoding,
        )
        self.__module_config_encoding_dropdown.installEventFilter(self)
        self.__module_config_encoding_dropdown.currentValueChanged.connect(
            lambda _: self.changed.emit()
        )
        behavior_settings_flayout.addRow(
            QLabel(self.tr("Encoding used for ModuleConfig.xml:")),
            self.__module_config_encoding_dropdown,
        )

    @override
    def eventFilter(self, source: QObject, event: QEvent) -> bool:
        if (
            event.type() == QEvent.Type.Wheel
            and (isinstance(source, QComboBox) or isinstance(source, QSpinBox))
            and isinstance(event, QWheelEvent)
        ):
            self.wheelEvent(event)
            return True

        return super().eventFilter(source, event)

    def __clear_history(self) -> None:
        self.__history.clear()
        self.__clear_history_button.setDisabled(True)

    def apply_settings(self) -> None:
        """
        Applies the current settings to the AppConfig.
        """

        self.__app_config.log_level = self.__log_level_box.getCurrentValue()
        self.__app_config.log_num_of_files = self.__log_num_of_files_box.value()
        self.__app_config.log_visible = self.__log_visible.isChecked()
        self.__app_config.language = self.__language_box.getCurrentValue()
        self.__app_config.ui_mode = self.__ui_mode_box.getCurrentValue()

        self.__behavior_config.finalize_on_save = self.__finalize_checkbox.isChecked()
        self.__behavior_config.validate_xml_on_save = (
            self.__validate_xml_checkbox.isChecked()
        )
        self.__behavior_config.module_config_encoding = (
            self.__module_config_encoding_dropdown.getCurrentValue()
        )
