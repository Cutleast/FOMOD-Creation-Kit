"""
Copyright (c) Cutleast
"""

from pathlib import Path

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem
from PySide6.QtWidgets import QLineEdit
from pytestqt.qtbot import QtBot

from core.fomod.fomod import Fomod
from core.fomod_editor.exceptions import (
    FileDoesNotExistError,
    ImageTypeNotSupportedError,
    NameIsMissingError,
)
from tests.utils import Utils
from ui.fomod_editor.info_editor_tab import InfoEditorTab
from ui.widgets.browse_edit import BrowseLineEdit
from ui.widgets.collapsible_text_edit import CollapsibleTextEdit
from ui.widgets.image_label import ImageLabel
from ui.widgets.url_edit import UrlEdit

from ..ui_test import UiTest


class TestInfoEditorTab(UiTest):
    """
    Tests `ui.fomod_editor.info_editor_tab.InfoEditorTab`.
    """

    NAME_ENTRY: tuple[str, type[QLineEdit]] = "name_entry", QLineEdit
    """Identifier for accessing the private name_entry field."""

    AUTHOR_ENTRY: tuple[str, type[QLineEdit]] = "author_entry", QLineEdit
    """Identifier for accessing the private author_entry field."""

    VERSION_ENTRY: tuple[str, type[QLineEdit]] = "version_entry", QLineEdit
    """Identifier for accessing the private version_entry field."""

    WEBSITE_ENTRY: tuple[str, type[UrlEdit]] = "website_entry", UrlEdit
    """Identifier for accessing the private website_entry field."""

    DESCRIPTION_ENTRY: tuple[str, type[CollapsibleTextEdit]] = (
        "description_entry",
        CollapsibleTextEdit,
    )
    """Identifier for accessing the private description_entry field."""

    IMAGE_PATH_ENTRY: tuple[str, type[BrowseLineEdit]] = (
        "image_path_entry",
        BrowseLineEdit,
    )
    """Identifier for accessing the private image_path_entry field."""

    IMAGE_LABEL: tuple[str, type[ImageLabel]] = "image_label", ImageLabel
    """Identifier for accessing the private image_label field."""

    @pytest.fixture
    def widget(self, qtbot: QtBot) -> InfoEditorTab:
        """
        Fixture that creates and provides an InfoEditorTab instance for tests.
        """

        widget = InfoEditorTab(Fomod.create(), None)
        qtbot.addWidget(widget)
        return widget

    def test_initial_state(self, widget: InfoEditorTab) -> None:
        """
        Tests the initial state of the widget.
        """

        # given
        name_entry: QLineEdit = Utils.get_private_field(
            widget, *TestInfoEditorTab.NAME_ENTRY
        )
        author_entry: QLineEdit = Utils.get_private_field(
            widget, *TestInfoEditorTab.AUTHOR_ENTRY
        )
        version_entry: QLineEdit = Utils.get_private_field(
            widget, *TestInfoEditorTab.VERSION_ENTRY
        )
        website_entry: UrlEdit = Utils.get_private_field(
            widget, *TestInfoEditorTab.WEBSITE_ENTRY
        )
        description_entry: CollapsibleTextEdit = Utils.get_private_field(
            widget, *TestInfoEditorTab.DESCRIPTION_ENTRY
        )
        image_path_entry: BrowseLineEdit = Utils.get_private_field(
            widget, *TestInfoEditorTab.IMAGE_PATH_ENTRY
        )

        # then
        assert name_entry.text() == ""
        assert author_entry.text() == ""
        assert version_entry.text() == ""
        assert website_entry.text() == ""
        assert description_entry.toPlainText() == ""
        assert image_path_entry.text() == ""

        with pytest.raises(NameIsMissingError):
            widget.validate()

    def test_edit_fomod_info(
        self, widget: InfoEditorTab, test_fs: FakeFilesystem
    ) -> None:
        """
        Tests the editing of a FOMOD info.
        """

        # given
        name_entry: QLineEdit = Utils.get_private_field(
            widget, *TestInfoEditorTab.NAME_ENTRY
        )
        author_entry: QLineEdit = Utils.get_private_field(
            widget, *TestInfoEditorTab.AUTHOR_ENTRY
        )
        version_entry: QLineEdit = Utils.get_private_field(
            widget, *TestInfoEditorTab.VERSION_ENTRY
        )
        website_entry: UrlEdit = Utils.get_private_field(
            widget, *TestInfoEditorTab.WEBSITE_ENTRY
        )
        description_entry: CollapsibleTextEdit = Utils.get_private_field(
            widget, *TestInfoEditorTab.DESCRIPTION_ENTRY
        )

        # when
        name_entry.setText("New Name")
        author_entry.setText("New Author")
        version_entry.setText("New Version")
        website_entry.setText("https://example.com")
        description_entry.setPlainText("New Description")

        # when
        widget.validate()
        fomod: Fomod = widget.save()

        # then
        assert fomod.name == "New Name"
        assert fomod.info.author == "New Author"
        assert fomod.info.version is not None
        assert fomod.info.version.version == "New Version"
        assert fomod.info.website == "https://example.com"
        assert fomod.info.description == "New Description"

        # when
        fomod.save_as(Path("fomod"), encoding="utf-16le")
        reloaded_fomod: Fomod = Fomod.load(Path("fomod"))

        # then
        assert reloaded_fomod.name == "New Name"
        assert reloaded_fomod.info.author == "New Author"
        assert reloaded_fomod.info.version is not None
        assert reloaded_fomod.info.version.version == "New Version"
        assert reloaded_fomod.info.website == "https://example.com"
        assert reloaded_fomod.info.description == "New Description"

    def test_validate(self, widget: InfoEditorTab, test_fs: FakeFilesystem) -> None:
        """
        Tests the validation of a FOMOD info.
        """

        # given
        name_entry: QLineEdit = Utils.get_private_field(
            widget, *TestInfoEditorTab.NAME_ENTRY
        )
        image_path_entry: BrowseLineEdit = Utils.get_private_field(
            widget, *TestInfoEditorTab.IMAGE_PATH_ENTRY
        )

        # when
        name_entry.setText("")

        # then
        with pytest.raises(NameIsMissingError):
            widget.validate()

        # when
        name_entry.setText("A valid name")

        # then
        widget.validate()

        # when
        image_path_entry.setText("A non existing file.txt")

        # then
        with pytest.raises(FileDoesNotExistError):
            widget.validate()

        # when
        Path("A non existing file.txt").touch()

        # then
        with pytest.raises(ImageTypeNotSupportedError):
            widget.validate()

        # when
        image_path_entry.setText("A valid image.png")
        Path("A valid image.png").touch()

        # then
        widget.validate()
