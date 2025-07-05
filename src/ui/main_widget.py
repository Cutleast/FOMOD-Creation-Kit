"""
Copyright (c) Cutleast
"""

from pathlib import Path
from typing import Optional, override

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QAbstractButton,
    QFileDialog,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from app_context import AppContext
from core.config.app_config import AppConfig
from core.config.behavior_config import BehaviorConfig
from core.fomod.fomod import Fomod
from core.fomod_editor.exceptions import ValidationError
from core.fomod_editor.history import History

from .fomod_editor.fomod_editor_widget import FomodEditorWidget


class MainWidget(QWidget):
    """
    Class for main widget.
    """

    changed = Signal(Fomod, bool)
    """
    Signal emitted when the user changes something at the FOMOD.
    
    Args:
        Fomod: The current FOMOD.
        bool: `True` if the FOMOD has changed, `False` if it was saved.
    """

    __changes_pending: bool = False

    app_config: AppConfig
    behavior_config: BehaviorConfig
    history: History

    __vlayout: QVBoxLayout
    __fomod_editor_widget: FomodEditorWidget

    def __init__(
        self, app_config: AppConfig, behavior_config: BehaviorConfig, history: History
    ) -> None:
        super().__init__()

        self.app_config = app_config
        self.behavior_config = behavior_config
        self.history = history

        self.__init_ui()
        self.__fomod_editor_widget.changed.connect(self.changed.emit)
        self.__fomod_editor_widget.changed.connect(self.__on_change)

    def __init_ui(self) -> None:
        self.__vlayout = QVBoxLayout()
        self.setLayout(self.__vlayout)

        self.__init_fomod_editor_widget()

    def __init_fomod_editor_widget(self) -> None:
        self.__fomod_editor_widget = FomodEditorWidget()
        self.__vlayout.addWidget(self.__fomod_editor_widget)

    def __on_change(self, fomod: Fomod, unsaved: bool) -> None:
        self.__changes_pending = unsaved

    def get_fomod_editor_widget(self) -> FomodEditorWidget:
        """
        Returns:
            FomodEditorWidget: The FOMOD editor widget.
        """

        return self.__fomod_editor_widget

    def open_fomod(self, path: Path) -> None:
        """
        Opens the FOMOD from the specified path.

        Args:
            path (Path): Path to a FOMOD installer.
        """

        if self.close():
            self.__open_fomod(path)

    def __open_fomod(self, path: Path) -> None:
        fomod: Fomod = Fomod.load(path)
        self.__fomod_editor_widget.set_fomod(fomod)
        if fomod.path is not None:
            self.history.add(fomod.path)

    def create_new_fomod(self) -> None:
        """
        Creates a new FOMOD and opens it in the FOMOD editor widget.
        """

        if self.close():
            fomod: Fomod = Fomod.create()
            self.__fomod_editor_widget.set_fomod(fomod)

    def open_fomod_from_file(self) -> None:
        """
        Opens a file dialog to load FOMOD from a file.
        """

        if self.close():
            file_dialog = QFileDialog(
                caption=self.tr("Load FOMOD installer from file...")
            )
            file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
            file_dialog.setNameFilters(
                [
                    self.tr("FOMOD metadata file") + " (info.xml)",
                    self.tr("FOMOD module config file") + " (ModuleConfig.xml)",
                ]
            )

            if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
                fomod_path = Path(file_dialog.selectedFiles()[0])
                self.__open_fomod(fomod_path)

    def open_fomod_from_folder(self) -> None:
        """
        Opens a file dialog to load FOMOD from a folder.
        """

        if self.close():
            file_dialog = QFileDialog(
                caption=self.tr("Load FOMOD installer from folder...")
            )
            file_dialog.setFileMode(QFileDialog.FileMode.Directory)

            if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
                fomod_path = Path(file_dialog.selectedFiles()[0])
                self.__open_fomod(fomod_path)

    def save_fomod(self) -> None:
        """
        Saves the FOMOD to its current path. Opens a file dialog to choose a path to save
        the current FOMOD installer to if it has no path, yet.
        """

        fomod: Optional[Fomod] = self.__fomod_editor_widget.get_fomod()

        if fomod is not None and fomod.path is None:
            self.save_fomod_as()

        elif fomod is not None:
            self.__fomod_editor_widget.save(
                finalize=self.behavior_config.finalize_on_save,
                validate_xml=self.behavior_config.validate_xml_on_save,
                encoding=self.behavior_config.module_config_encoding.value,
            )

    def save_fomod_as(self) -> None:
        """
        Opens a file dialog to choose a path to save the current FOMOD installer to.
        """

        file_dialog = QFileDialog(caption=self.tr("Save FOMOD installer as..."))
        file_dialog.setFileMode(QFileDialog.FileMode.Directory)

        if file_dialog.exec() == QFileDialog.DialogCode.Accepted:
            fomod_path = Path(file_dialog.selectedFiles()[0])
            if fomod_path.parts[-1].lower() != "fomod":
                fomod_path /= "fomod"
            self.__fomod_editor_widget.save(
                finalize=self.behavior_config.finalize_on_save,
                path=fomod_path,
                validate_xml=self.behavior_config.validate_xml_on_save,
                encoding=self.behavior_config.module_config_encoding.value,
            )
            self.history.add(fomod_path)

    @override
    def close(self) -> bool:
        """
        Attempts to close the current FOMOD and asks the user if unsaved changes should
        be lost.

        Returns:
            bool:
                `True` if there are no unsaved changes or the user chose to close,
                `False` otherwise.
        """

        if self.__changes_pending:
            match self.__show_close_unsaved_messagebox():
                case QMessageBox.StandardButton.No:
                    return False
                case QMessageBox.StandardButton.Discard:
                    return True
                case QMessageBox.StandardButton.Save:
                    self.save_fomod()
                    return True

        return True

    def __show_close_unsaved_messagebox(self) -> QMessageBox.StandardButton:
        valid: bool = False

        try:
            self.__fomod_editor_widget.validate()
            valid = True
        except ValidationError:
            pass

        message_box = QMessageBox(self)
        message_box.setWindowTitle(self.tr("Close unsaved FOMOD?"))
        message_box.setText(
            self.tr(
                "Are you sure you want to close the current FOMOD? "
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

        no_button: QAbstractButton = message_box.button(QMessageBox.StandardButton.No)
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
        message_box.setStyleSheet(AppContext.get_app().styleSheet())

        return QMessageBox.StandardButton(message_box.exec())
