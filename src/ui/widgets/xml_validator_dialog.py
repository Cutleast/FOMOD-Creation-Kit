"""
Copyright (c) Cutleast
"""

from pathlib import Path
from typing import Optional

from lxml import etree
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QFileDialog,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from core.utilities.xml import validate_against_schema
from ui.widgets.browse_edit import BrowseLineEdit


class XmlValidatorDialog(QDialog):
    """
    Dialog for validating XML files against a specified XSD schema.
    """

    __vlayout: QVBoxLayout

    __xml_path_entry: BrowseLineEdit
    __xsd_url_entry: QLineEdit

    __validate_button: QPushButton

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)

        self.setWindowTitle(self.tr("Validate XML file against XSD schema"))
        self.resize(700, 150)

        self.__init_ui()

        self.__xml_path_entry.textChanged.connect(lambda text: self.__on_change())
        self.__xsd_url_entry.textChanged.connect(lambda text: self.__on_change())
        self.__validate_button.clicked.connect(self.__run_validation)

    def __init_ui(self) -> None:
        self.__vlayout = QVBoxLayout()
        self.__vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.setLayout(self.__vlayout)

        self.__init_form()
        self.__init_footer()

    def __init_form(self) -> None:
        flayout = QFormLayout()
        self.__vlayout.addLayout(flayout)

        self.__xml_path_entry = BrowseLineEdit()
        self.__xml_path_entry.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.__xml_path_entry.setNameFilters([self.tr("XML Files") + " (*.xml)"])
        flayout.addRow(self.tr("Path to XML file:"), self.__xml_path_entry)

        self.__xsd_url_entry = QLineEdit()
        flayout.addRow(self.tr("URL to XSD schema:"), self.__xsd_url_entry)

    def __init_footer(self) -> None:
        self.__validate_button = QPushButton(self.tr("Validate"))
        self.__validate_button.setDefault(True)
        self.__validate_button.setDisabled(True)
        self.__vlayout.addWidget(self.__validate_button)

    def __on_change(self) -> None:
        self.__validate_button.setEnabled(
            bool(
                Path(self.__xml_path_entry.text()).is_file()
                and self.__xsd_url_entry.text().strip()
            )
        )
        self.__validate_button.setText(self.tr("Validate"))

    def __run_validation(self) -> None:
        xml_text: bytes = Path(self.__xml_path_entry.text()).read_bytes()
        xsd_url: str = self.__xsd_url_entry.text().strip()

        try:
            validate_against_schema(xsd_url, xml_text)
        except etree.DocumentInvalid as ex:
            self.__validate_button.setText(self.tr("Invalid: ") + str(ex))
        else:
            self.__validate_button.setText(self.tr("Valid"))

        self.__validate_button.setDisabled(True)
