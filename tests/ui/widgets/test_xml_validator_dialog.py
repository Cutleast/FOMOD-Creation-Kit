"""
Copyright (c) Cutleast
"""

from pathlib import Path

import pytest
from PySide6.QtWidgets import QLineEdit, QPushButton
from pytestqt.qtbot import QtBot

from core.fomod.module_config.module_config import ModuleConfig
from tests.utils import Utils
from ui.widgets.browse_edit import BrowseLineEdit
from ui.widgets.xml_validator_dialog import XmlValidatorDialog

from ..ui_test import UiTest


class TestXmlValidatorDialog(UiTest):
    """
    Tests `ui.widgets.xml_validator_dialog.XmlValidatorDialog`.
    """

    XML_PATH_ENTRY: tuple[str, type[BrowseLineEdit]] = (
        "xml_path_entry",
        BrowseLineEdit,
    )
    """Identifier for accessing the private xml_path_entry field."""

    XSD_URL_ENTRY: tuple[str, type[QLineEdit]] = ("xsd_url_entry", QLineEdit)
    """Identifier for accessing the private xsd_url_entry field."""

    VALIDATE_BUTTON: tuple[str, type[QPushButton]] = ("validate_button", QPushButton)
    """Identifier for accessing the private validate_button field."""

    @pytest.fixture
    def widget(self, qtbot: QtBot) -> XmlValidatorDialog:
        """
        Fixture to create and provide a XmlValidatorDialog instance for tests.
        """

        xml_validator_dialog = XmlValidatorDialog()
        qtbot.addWidget(xml_validator_dialog)
        xml_validator_dialog.show()
        return xml_validator_dialog

    def test_initial_state(self, widget: XmlValidatorDialog) -> None:
        """
        Tests the initial state of the XmlValidatorDialog.
        """

        # given
        xml_path_entry: BrowseLineEdit = Utils.get_private_field(
            widget, *TestXmlValidatorDialog.XML_PATH_ENTRY
        )
        xsd_url_entry: QLineEdit = Utils.get_private_field(
            widget, *TestXmlValidatorDialog.XSD_URL_ENTRY
        )
        validate_button: QPushButton = Utils.get_private_field(
            widget, *TestXmlValidatorDialog.VALIDATE_BUTTON
        )

        # then
        assert xml_path_entry.text() == ""
        assert xsd_url_entry.text() == ""
        assert validate_button.text() == "Validate"
        assert not validate_button.isEnabled()

    def test_input_change_updates_validate_button(
        self, data_folder: Path, widget: XmlValidatorDialog
    ) -> None:
        """
        Tests that changes to the XML path and XSD URL entries update the validate
        button.
        """

        # given
        xml_path_entry: BrowseLineEdit = Utils.get_private_field(
            widget, *TestXmlValidatorDialog.XML_PATH_ENTRY
        )
        xsd_url_entry: QLineEdit = Utils.get_private_field(
            widget, *TestXmlValidatorDialog.XSD_URL_ENTRY
        )
        validate_button: QPushButton = Utils.get_private_field(
            widget, *TestXmlValidatorDialog.VALIDATE_BUTTON
        )
        xml_file_path: Path = data_folder / "TestModuleConfig" / "ModuleConfig.xml"
        schema_url: str = ModuleConfig.get_schema_url()

        # when
        xml_path_entry.setText(str(xml_file_path))

        # then
        assert not validate_button.isEnabled()
        assert validate_button.text() == "Validate"

        # when
        xsd_url_entry.setText(schema_url)

        # then
        assert validate_button.isEnabled()
        assert validate_button.text() == "Validate"

    def test_run_validation_updates_validate_button(
        self, data_folder: Path, widget: XmlValidatorDialog
    ) -> None:
        """
        Tests that running the validation by clicking on the validate button updates the
        validate button and sets its text to "Valid".
        """

        # given
        xml_path_entry: BrowseLineEdit = Utils.get_private_field(
            widget, *TestXmlValidatorDialog.XML_PATH_ENTRY
        )
        xsd_url_entry: QLineEdit = Utils.get_private_field(
            widget, *TestXmlValidatorDialog.XSD_URL_ENTRY
        )
        validate_button: QPushButton = Utils.get_private_field(
            widget, *TestXmlValidatorDialog.VALIDATE_BUTTON
        )
        xml_file_path: Path = data_folder / "TestModuleConfig" / "ModuleConfig.xml"
        schema_url: str = ModuleConfig.get_schema_url()

        # when
        xml_path_entry.setText(str(xml_file_path))
        xsd_url_entry.setText(schema_url)
        validate_button.click()

        # then
        assert not validate_button.isEnabled()
        assert validate_button.text() == "Valid" or validate_button.text().startswith(
            "Error:"
        )
