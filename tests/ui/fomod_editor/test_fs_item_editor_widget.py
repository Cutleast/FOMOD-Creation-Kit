"""
Copyright (c) Cutleast
"""

from pathlib import Path

import pytest
from cutleast_core_lib.ui.widgets.browse_edit import BrowseLineEdit
from cutleast_core_lib.ui.widgets.enum_radiobutton_widget import EnumRadiobuttonsWidget
from pyfakefs.fake_filesystem import FakeFilesystem
from PySide6.QtWidgets import QCheckBox, QFileDialog, QLineEdit, QSpinBox
from pytestqt.qtbot import QtBot

from core.fomod.module_config.file_system.file_item import FileItem
from core.fomod.module_config.file_system.folder_item import FolderItem
from core.fomod_editor.exceptions import SpecificEmptyError, SpecificValidationError
from tests.base_test import BaseTest
from tests.utils import Utils
from ui.fomod_editor.fs_item_editor_widget import FsItemEditorWidget


class TestFsItemEditorWidget(BaseTest):
    """
    Tests `ui.fomod_editor.fs_item_editor_widget.FsItemEditorWidget`.
    """

    SOURCE_ENTRY: tuple[str, type[BrowseLineEdit]] = "source_entry", BrowseLineEdit
    """Identifier for accessing the private source_entry field."""

    TYPE_SELECTOR: tuple[
        str, type[EnumRadiobuttonsWidget[FsItemEditorWidget.ItemType]]
    ] = ("type_selector", EnumRadiobuttonsWidget)
    """Identifier for accessing the private type_selector field."""

    DESTINATION_ENTRY: tuple[str, type[QLineEdit]] = "destination_entry", QLineEdit
    """Identifier for accessing the private destination_entry field."""

    ALWAYS_INSTALL_CHECKBOX: tuple[str, type[QCheckBox]] = (
        "always_install_checkbox",
        QCheckBox,
    )
    """Identifier for accessing the private always_install_checkbox field."""

    INSTALL_IF_USABLE_CHECKBOX: tuple[str, type[QCheckBox]] = (
        "install_if_usable_checkbox",
        QCheckBox,
    )
    """Identifier for accessing the private install_if_usable_checkbox field."""

    PRIORITY_ENTRY: tuple[str, type[QSpinBox]] = "priority_entry", QSpinBox
    """Identifier for accessing the private priority_entry field."""

    BROWSE_EDIT_FILE_MODE: tuple[str, type[QFileDialog.FileMode]] = (
        "file_mode",
        QFileDialog.FileMode,
    )
    """Identifier for accessing the private file_mode field of a BrowseLineEdit."""

    @pytest.fixture
    def widget(self, qtbot: QtBot) -> FsItemEditorWidget:
        """
        Fixture that creates and provides a FsItemEditorWidget instance with a blank
        file item for tests.
        """

        fs_item_editor_widget = FsItemEditorWidget(FileItem.create(), None, list)
        qtbot.addWidget(fs_item_editor_widget)
        return fs_item_editor_widget

    def test_initial_state(self, widget: FsItemEditorWidget) -> None:
        """
        Tests the initial state of the widget.
        """

        # given
        source_entry: BrowseLineEdit = Utils.get_private_field(
            widget, *TestFsItemEditorWidget.SOURCE_ENTRY
        )
        type_selector: EnumRadiobuttonsWidget[FsItemEditorWidget.ItemType] = (
            Utils.get_private_field(widget, *TestFsItemEditorWidget.TYPE_SELECTOR)
        )
        destination_entry: QLineEdit = Utils.get_private_field(
            widget, *TestFsItemEditorWidget.DESTINATION_ENTRY
        )
        always_install_checkbox: QCheckBox = Utils.get_private_field(
            widget, *TestFsItemEditorWidget.ALWAYS_INSTALL_CHECKBOX
        )
        install_if_usable_checkbox: QCheckBox = Utils.get_private_field(
            widget, *TestFsItemEditorWidget.INSTALL_IF_USABLE_CHECKBOX
        )
        priority_entry: QSpinBox = Utils.get_private_field(
            widget, *TestFsItemEditorWidget.PRIORITY_ENTRY
        )

        # then
        assert source_entry.text() == ""
        assert type_selector.getCurrentValue() == FsItemEditorWidget.ItemType.File
        assert destination_entry.text() == ""
        assert not always_install_checkbox.isChecked()
        assert not install_if_usable_checkbox.isChecked()
        assert priority_entry.value() == 0

        with pytest.raises(
            SpecificEmptyError, match="The source path must not be empty!"
        ):
            widget.validate()

    def test_validation_for_existing_source(
        self, test_fs: FakeFilesystem, widget: FsItemEditorWidget
    ) -> None:
        """
        Tests the validation for an existing source file or folder.
        """

        # given
        source_entry: BrowseLineEdit = Utils.get_private_field(
            widget, *TestFsItemEditorWidget.SOURCE_ENTRY
        )
        type_selector: EnumRadiobuttonsWidget[FsItemEditorWidget.ItemType] = (
            Utils.get_private_field(widget, *TestFsItemEditorWidget.TYPE_SELECTOR)
        )

        # when/then
        with pytest.raises(
            SpecificEmptyError, match="The source path must not be empty!"
        ):
            widget.validate()

        # when
        source_entry.setText("Test Folder")

        # then
        with pytest.raises(
            SpecificValidationError,
            match=r'The source path \("Test Folder"\) must be an existing file!',
        ):
            widget.validate()

        # when
        Path("Test Folder").mkdir()

        # then
        with pytest.raises(
            SpecificValidationError,
            match=r'The source path \("Test Folder"\) must be an existing file!',
        ):
            widget.validate()

        # when
        type_selector.setCurrentValue(FsItemEditorWidget.ItemType.Folder)

        # then
        widget.validate()

        # when
        source_entry.setText("Test File")

        # then
        with pytest.raises(
            SpecificValidationError,
            match=r'The source path \("Test File"\) must be an existing folder!',
        ):
            widget.validate()

        # when
        Path("Test File").touch()

        # then
        with pytest.raises(
            SpecificValidationError,
            match=r'The source path \("Test File"\) must be an existing folder!',
        ):
            widget.validate()

        # when
        type_selector.setCurrentValue(FsItemEditorWidget.ItemType.File)

        # then
        widget.validate()

    def test_correct_initial_file_mode(self, qtbot: QtBot) -> None:
        """
        Tests that the widget initializes correctly in file mode.
        """

        # given
        file_item: FileItem = FileItem.create()
        widget = FsItemEditorWidget(file_item, None, list)
        qtbot.addWidget(widget)

        source_entry: BrowseLineEdit = Utils.get_private_field(
            widget, *TestFsItemEditorWidget.SOURCE_ENTRY
        )
        source_file_mode: QFileDialog.FileMode = Utils.get_private_field(
            source_entry, *TestFsItemEditorWidget.BROWSE_EDIT_FILE_MODE
        )
        type_selector: EnumRadiobuttonsWidget[FsItemEditorWidget.ItemType] = (
            Utils.get_private_field(widget, *TestFsItemEditorWidget.TYPE_SELECTOR)
        )

        # then
        assert source_file_mode == QFileDialog.FileMode.ExistingFile
        assert type_selector.getCurrentValue() == FsItemEditorWidget.ItemType.File

        # when
        folder_item: FolderItem = FolderItem.create()
        widget = FsItemEditorWidget(folder_item, None, list)
        qtbot.addWidget(widget)

        source_entry = Utils.get_private_field(
            widget, *TestFsItemEditorWidget.SOURCE_ENTRY
        )
        source_file_mode = Utils.get_private_field(
            source_entry, *TestFsItemEditorWidget.BROWSE_EDIT_FILE_MODE
        )
        type_selector = Utils.get_private_field(
            widget, *TestFsItemEditorWidget.TYPE_SELECTOR
        )

        # then
        assert source_file_mode == QFileDialog.FileMode.Directory
        assert type_selector.getCurrentValue() == FsItemEditorWidget.ItemType.Folder
