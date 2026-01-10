"""
Copyright (c) Cutleast
"""

from typing import override

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QCloseEvent
from PySide6.QtWidgets import (
    QAbstractButton,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from core.fomod_editor.exceptions import ValidationError
from ui.utilities.theme_manager import ThemeManager

from .base_editor_widget import BaseEditorWidget


class EditorWindow[T: BaseEditorWidget](QWidget):
    """
    Non-modal window wrapping a FOMOD editor widget. Handles saving and validation.
    """

    saved = Signal()
    """Signal emitted when the edited item is saved."""

    closed = Signal()
    """Signal emitted when the window is closed."""

    __changes_pending: bool = False

    __vlayout: QVBoxLayout
    __editor_widget: T
    __validation_status_label: QLabel

    def __init__(self, editor_widget: T, validate_on_init: bool = False) -> None:
        """
        Args:
            editor_widget (T): FOMOD editor widget to wrap in a dialog.
            validate_on_init (bool, optional):
                Whether to validate (and enable the save button) on initialization.
                Defaults to False.
        """

        super().__init__()

        self.setWindowFlag(Qt.WindowType.Window, True)
        self.setWindowTitle(editor_widget.get_display_name())

        self.__editor_widget = editor_widget

        self.__init_ui()
        self.__editor_widget.changed.connect(self.__on_change)
        self.__editor_widget.discarded.connect(self.__on_discard)

        if validate_on_init:
            self.__update_save_button()

    def __init_ui(self) -> None:
        self.__vlayout = QVBoxLayout()
        self.setLayout(self.__vlayout)

        self.__vlayout.addWidget(self.__editor_widget)

        self.__init_footer()

        self.setMinimumHeight(
            max(
                self.__editor_widget.baseSize().height(),
                self.__editor_widget.minimumHeight(),
            )
            + 50
        )
        self.setMinimumWidth(
            max(
                self.__editor_widget.baseSize().width(),
                self.__editor_widget.minimumWidth(),
            )
        )

    def __init_footer(self) -> None:
        hlayout = QHBoxLayout()
        self.__vlayout.addLayout(hlayout)

        cancel_button = QPushButton(self.tr("Cancel"))
        cancel_button.clicked.connect(self.close)
        hlayout.addWidget(cancel_button)

        self.__validation_status_label = QLabel()
        self.__validation_status_label.setObjectName("status_label")
        self.__validation_status_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
        )
        self.__validation_status_label.setWordWrap(True)
        # prevent label from increasing the window's size
        self.__validation_status_label.setMinimumWidth(50)
        hlayout.addWidget(self.__validation_status_label, stretch=1)

        self.__save_button = QPushButton(self.tr("Save"))
        self.__save_button.setDefault(True)
        self.__save_button.clicked.connect(self.__save_and_close)
        self.__save_button.setDisabled(True)
        hlayout.addWidget(self.__save_button)

    def __save_and_close(self) -> None:
        self.__save()
        self.close()

    @override
    def closeEvent(self, event: QCloseEvent) -> None:
        valid: bool = self.__save_button.isEnabled()

        if self.__changes_pending:
            message_box = QMessageBox(self)
            message_box.setWindowTitle(self.tr("Close unsaved item?"))
            message_box.setText(
                self.tr(
                    "Are you sure you want to close the current item? "
                    "There are unsaved changes that will be lost."
                )
            )
            if valid:
                message_box.setStandardButtons(
                    QMessageBox.StandardButton.No
                    | QMessageBox.StandardButton.Discard
                    | QMessageBox.StandardButton.Save
                )
                message_box.setDefaultButton(QMessageBox.StandardButton.Save)
            else:
                message_box.setStandardButtons(
                    QMessageBox.StandardButton.No | QMessageBox.StandardButton.Discard
                )
                message_box.setDefaultButton(QMessageBox.StandardButton.No)

            no_button: QAbstractButton = message_box.button(
                QMessageBox.StandardButton.No
            )
            no_button.setText(self.tr("No"))
            yes_button: QAbstractButton = message_box.button(
                QMessageBox.StandardButton.Discard
            )
            yes_button.setText(self.tr("Yes"))
            if valid:
                save_button: QAbstractButton = message_box.button(
                    QMessageBox.StandardButton.Save
                )
                save_button.setText(self.tr("Save and close"))

            # Reapply stylesheet as setObjectName() doesn't update the style by itself
            message_box.setStyleSheet(ThemeManager.get_stylesheet() or "")

            match message_box.exec():
                case QMessageBox.StandardButton.Discard:
                    self.__editor_widget.discard()
                    self.saved.disconnect()
                    return event.accept()
                case QMessageBox.StandardButton.Save:
                    self.__save()
                    self.saved.disconnect()
                    return event.accept()

            event.ignore()

        else:
            self.saved.disconnect()
            event.accept()

    def __on_change(self) -> None:
        self.__changes_pending = True
        self.setWindowTitle(self.__editor_widget.get_display_name() + "*")

        self.__update_save_button()

    def __on_discard(self) -> None:
        self.__changes_pending = False
        self.setWindowTitle(self.__editor_widget.get_display_name())

        self.__update_save_button()

    def __save(self) -> None:
        self.__editor_widget.save()
        self.__changes_pending = False
        self.saved.emit()

    def __update_save_button(self) -> None:
        try:
            self.__editor_widget.validate()
            self.__save_button.setEnabled(True)
            self.__validation_status_label.setText("")
        except ValidationError as ex:
            self.__save_button.setDisabled(True)
            self.__validation_status_label.setText(str(ex))

    def show_and_activate(self) -> None:
        """
        Shows and activates the window. If the window is minimized, it is restored and
        then activated (request focus).
        """

        self.showNormal()
        self.activateWindow()
