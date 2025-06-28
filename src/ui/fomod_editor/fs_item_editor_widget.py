"""
Copyright (c) Cutleast
"""

from pathlib import Path
from typing import Optional, override

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLineEdit,
    QSpinBox,
)

from core.fomod.module_config.file_item import FileItem
from core.fomod.module_config.file_system.file_system_item import FileSystemItem
from core.fomod.module_config.folder_item import FolderItem
from core.fomod_editor.exceptions import SpecificEmptyError, SpecificValidationError
from core.utilities.path import get_joined_path_if_relative
from ui.widgets.browse_edit import BrowseLineEdit
from ui.widgets.enum_dropdown import LocalizedEnum
from ui.widgets.enum_radiobutton_widget import EnumRadiobuttonsWidget

from .base_editor_widget import BaseEditorWidget


class FsItemEditorWidget(BaseEditorWidget[FileSystemItem]):
    """
    Widget for editing a file system item.
    """

    __source_entry: BrowseLineEdit

    class ItemType(LocalizedEnum):
        """Enum for the possible file system item types."""

        File = 0
        """A file."""

        Folder = 1
        """A folder."""

        @override
        def get_localized_name(self) -> str:
            locs: dict[FsItemEditorWidget.ItemType, str] = {
                FsItemEditorWidget.ItemType.File: QApplication.translate(
                    "FsItemEditorWidget", "File"
                ),
                FsItemEditorWidget.ItemType.Folder: QApplication.translate(
                    "FsItemEditorWidget", "Folder"
                ),
            }

            return locs[self]

        @override
        def get_localized_description(self) -> str:
            return ""

    __type_selector: EnumRadiobuttonsWidget[ItemType]

    __destination_entry: QLineEdit
    __always_install_checkbox: QCheckBox
    __install_if_usable_checkbox: QCheckBox
    __priority_entry: QSpinBox

    @override
    def _post_init(self) -> None:
        self.__source_entry.textChanged.connect(lambda _: self.changed.emit())
        self.__type_selector.currentValueChanged.connect(
            lambda item_type: self.__source_entry.setFileMode(
                QFileDialog.FileMode.ExistingFile
                if item_type == FsItemEditorWidget.ItemType.File
                else QFileDialog.FileMode.Directory
            )
        )
        self.__type_selector.currentValueChanged.connect(lambda _: self.changed.emit())

        self.__destination_entry.textChanged.connect(lambda _: self.changed.emit())
        self.__always_install_checkbox.stateChanged.connect(
            lambda _: self.changed.emit()
        )
        self.__install_if_usable_checkbox.stateChanged.connect(
            lambda _: self.changed.emit()
        )
        self.__priority_entry.valueChanged.connect(lambda _: self.changed.emit())

    @override
    @classmethod
    def get_display_name(cls) -> str:
        return QApplication.translate("FsItemEditorWidget", "Edit file system item...")

    @override
    @classmethod
    def get_description(cls) -> str:
        return QApplication.translate(
            "FsItemEditorWidget",
            "A file or folder to be copied to a destination folder.",
        )

    @override
    def _init_ui(self) -> None:
        super()._init_ui()

        self.__init_form()

        self.setBaseSize(700, 280)

    def __init_form(self) -> None:
        flayout = QFormLayout()
        flayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        flayout.setContentsMargins(0, 0, 0, 0)
        self._vlayout.addLayout(flayout)

        hlayout = QHBoxLayout()
        hlayout.setContentsMargins(0, 0, 0, 0)
        self.__source_entry = BrowseLineEdit()
        self.__source_entry.setToolTip(
            self.tr("The path to the file or folder in the FOMOD folder.")
        )
        self.__source_entry.setPlaceholderText(self.tr('eg. "..\\core\\test.esp"'))
        if self._item.source != Path("__default__"):
            self.__source_entry.setText(str(self._item.source))
        hlayout.addWidget(self.__source_entry)

        self.__type_selector = EnumRadiobuttonsWidget(
            FsItemEditorWidget.ItemType,
            FsItemEditorWidget.ItemType.File
            if isinstance(self._item, FileItem)
            else FsItemEditorWidget.ItemType.Folder,
            orientation=Qt.Orientation.Horizontal,
        )
        hlayout.addWidget(self.__type_selector)
        flayout.addRow(self.tr("Source:"), hlayout)

        self.__destination_entry = QLineEdit()
        self.__destination_entry.setToolTip(
            self.tr(
                "The path to which the file or folder should be installed. If omitted, "
                "the destination is the same as the source."
            )
        )
        self.__destination_entry.setPlaceholderText(
            self.tr('eg. "test.esp" (leave empty to be the same as the source)')
        )
        if self._item.destination is not None:
            self.__destination_entry.setText(str(self._item.destination))
        flayout.addRow(self.tr("Destination (optional):"), self.__destination_entry)

        self.__always_install_checkbox = QCheckBox(self.tr("Always install"))
        self.__always_install_checkbox.setToolTip(
            self.tr(
                "Indicates that the file or folder should always be installed, "
                "regardless of whether or not the plugin has been selected."
            )
        )
        self.__always_install_checkbox.setChecked(self._item.always_install)
        flayout.addRow(self.__always_install_checkbox)

        self.__install_if_usable_checkbox = QCheckBox(self.tr("Install if usable"))
        self.__install_if_usable_checkbox.setToolTip(
            self.tr(
                "Indicates that the file or folder should always be installed if the "
                "plugin is not NotUsable, regardless of whether or not the plugin has "
                "been selected."
            )
        )
        self.__install_if_usable_checkbox.setChecked(self._item.install_if_usable)
        flayout.addRow(self.__install_if_usable_checkbox)

        self.__priority_entry = QSpinBox()
        self.__priority_entry.setToolTip(
            self.tr(
                "A number describing the relative priority of the file or folder. A "
                "higher number indicates the file or folder should be installed after "
                "the items with lower numbers. This value does not have to be unique."
            )
        )
        self.__priority_entry.setRange(0, 1000)
        self.__priority_entry.setValue(self._item.priority)
        flayout.addRow(self.tr("Priority:"), self.__priority_entry)

    @override
    def validate(self) -> None:
        if not self.__source_entry.text().strip():
            raise SpecificEmptyError(self.tr("The source path must not be empty!"))

        source_path: Path = get_joined_path_if_relative(
            Path(self.__source_entry.text().strip()),
            base_path=self._fomod_path.parent if self._fomod_path is not None else None,
        )
        if self.__type_selector.getCurrentValue() == FsItemEditorWidget.ItemType.File:
            if not source_path.is_file():
                raise SpecificValidationError(
                    self.tr('The source path ("{0}") must be an existing file!').format(
                        source_path
                    )
                )
        else:
            if not source_path.is_dir():
                raise SpecificValidationError(
                    self.tr(
                        'The source path ("{0}") must be an existing folder!'
                    ).format(source_path)
                )

    @override
    def save(self) -> FileSystemItem:
        source = Path(self.__source_entry.text().strip())
        destination: Optional[Path] = (
            Path(self.__destination_entry.text().strip())
            if self.__destination_entry.text().strip()
            else None
        )
        always_install: bool = self.__always_install_checkbox.isChecked()
        install_if_usable: bool = self.__install_if_usable_checkbox.isChecked()
        priority: int = self.__priority_entry.value()

        if self.__type_selector.getCurrentValue() == FsItemEditorWidget.ItemType.File:
            self._item = FileItem(
                source=source,
                destination=destination,
                always_install=always_install,
                install_if_usable=install_if_usable,
                priority=priority,
            )
        else:
            self._item = FolderItem(
                source=source,
                destination=destination,
                always_install=always_install,
                install_if_usable=install_if_usable,
                priority=priority,
            )

        self.saved.emit(self._item)
        return self._item
