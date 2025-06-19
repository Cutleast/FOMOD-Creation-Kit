"""
Copyright (c) Cutleast
"""

from pathlib import Path
from typing import Optional, override

import qtawesome as qta
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QFileDialog, QFormLayout, QLabel, QLineEdit

from core.fomod.fomod import Fomod
from core.fomod.module_config.header_image import SUPPORTED_TYPES, HeaderImage
from core.fomod_editor.exceptions import (
    FileDoesNotExistError,
    ImageTypeNotSupportedError,
    NameIsMissingError,
)
from ui.widgets.browse_edit import BrowseLineEdit
from ui.widgets.collapsible_text_edit import CollapsibleTextEdit
from ui.widgets.image_label import ImageLabel
from ui.widgets.url_edit import UrlEdit

from .base_editor_widget import BaseEditorWidget


class InfoEditorTab(BaseEditorWidget[Fomod]):
    """
    Widget for editing the metadata of a FOMOD installer.
    """

    IMAGE_HEIGHT: int = 300
    """The height in pixels of the displayed image."""

    __flayout: QFormLayout

    __name_entry: QLineEdit
    __author_entry: QLineEdit
    __version_entry: QLineEdit
    __website_entry: UrlEdit
    __description_entry: CollapsibleTextEdit
    __image_path_entry: BrowseLineEdit
    __image_label: ImageLabel

    def __init__(self, item: Fomod, fomod_path: Optional[Path]) -> None:
        super().__init__(item, fomod_path)

        self.__name_entry.textChanged.connect(lambda text: self.changed.emit())
        self.__author_entry.textChanged.connect(lambda text: self.changed.emit())
        self.__version_entry.textChanged.connect(lambda text: self.changed.emit())
        self.__website_entry.textChanged.connect(lambda text: self.changed.emit())
        self.__description_entry.textChanged.connect(self.changed.emit)
        self.__image_path_entry.textChanged.connect(lambda text: self.changed.emit())
        self.__image_path_entry.textChanged.connect(
            lambda text: self.__on_image_path_change()
        )

        if (
            self._item.module_config.module_image is not None
            and self._item.module_config.module_image.path is not None
            and self._item.path is not None
        ):
            self.__image_path_entry.setText(
                str(self._item.module_config.module_image.path)
            )

    @override
    @classmethod
    def get_display_name(cls) -> str:
        return QApplication.translate("InfoEditorTab", "Edit FOMOD info...")

    @override
    def _init_ui(self) -> None:
        super()._init_ui()

        self.__flayout = QFormLayout()
        self.__flayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.__flayout.setContentsMargins(5, 5, 5, 5)
        self._vlayout.addLayout(self.__flayout)

        self.__init_form()

        placeholder = QLabel()
        placeholder.setMinimumHeight(0)
        placeholder.setBaseSize(0, 0)
        self.__flayout.addRow(placeholder)

    def __init_form(self) -> None:
        self.__image_label = ImageLabel(
            qta.icon("mdi6.image-off-outline", color="#666666").pixmap(
                InfoEditorTab.IMAGE_HEIGHT, InfoEditorTab.IMAGE_HEIGHT
            ),
            round_pixmap=True,
        )
        self.__image_label.setFixedHeight(InfoEditorTab.IMAGE_HEIGHT)
        self.__flayout.addRow(self.__image_label)

        self.__name_entry = QLineEdit()
        self.__name_entry.setText(self._item.name)
        self.__flayout.addRow(self.tr("Name:"), self.__name_entry)

        self.__author_entry = QLineEdit()
        self.__author_entry.setText(self._item.info.author)
        self.__flayout.addRow(self.tr("Author:"), self.__author_entry)

        self.__version_entry = QLineEdit()
        self.__version_entry.setText(self._item.info.version.version)
        self.__flayout.addRow(self.tr("Version:"), self.__version_entry)

        self.__website_entry = UrlEdit()
        self.__website_entry.setText(self._item.info.website)
        self.__flayout.addRow(self.tr("Website:"), self.__website_entry)

        self.__description_entry = CollapsibleTextEdit()
        self.__description_entry.setPlainText(self._item.info.description)
        # this is required to "adjust" the height correctly
        self.__description_entry.setExpanded(False)
        self.__description_entry.setExpanded(True)
        self.__flayout.addRow(self.tr("Description:"), self.__description_entry)

        self.__image_path_entry = BrowseLineEdit()
        self.__image_path_entry.setFileMode(QFileDialog.FileMode.ExistingFile)
        self.__image_path_entry.setNameFilters(
            [self.tr("Image Files") + f" (*{' *'.join(SUPPORTED_TYPES)})"]
        )
        self.__flayout.addRow(self.tr("Image:"), self.__image_path_entry)

    def __on_image_path_change(self) -> None:
        image_path: Optional[Path] = (
            Path(self.__image_path_entry.text().strip())
            if self.__image_path_entry.text().strip()
            else None
        )

        if (
            image_path is not None
            and not image_path.is_absolute()
            and self._item.path is not None
        ):
            image_path = self._item.path.parent / image_path

        if image_path is not None and image_path.is_file():
            self.__image_label.setPixmap(QPixmap(str(image_path)))
        else:
            self.__image_label.setPixmap(
                qta.icon("mdi6.image-off-outline", color="#666666").pixmap(
                    InfoEditorTab.IMAGE_HEIGHT, InfoEditorTab.IMAGE_HEIGHT
                )
            )

    @override
    def save(self) -> Fomod:
        self._item.name = self.__name_entry.text()
        self._item.info.author = self.__author_entry.text()
        self._item.info.version.version = self.__version_entry.text()
        self._item.info.website = self.__website_entry.text()
        self._item.info.description = self.__description_entry.toPlainText()

        image_path: Optional[Path] = (
            Path(self.__image_path_entry.text().strip())
            if self.__image_path_entry.text().strip()
            else None
        )
        if image_path is not None and self._item.path is not None:
            if self._item.module_config.module_image is None:
                self._item.module_config.module_image = HeaderImage()
            if image_path.is_relative_to(self._item.path.parent):
                image_path = image_path.relative_to(self._item.path.parent)
            self._item.module_config.module_image.path = image_path
        else:
            self._item.module_config.module_image = None

        self.saved.emit(self._item)
        return self._item

    @override
    def validate(self) -> None:
        if not self.__name_entry.text().strip():
            raise NameIsMissingError

        image_path: Optional[Path] = (
            Path(self.__image_path_entry.text().strip())
            if self.__image_path_entry.text().strip()
            else None
        )

        if image_path is not None and self._item.path is not None:
            if not image_path.is_absolute():
                image_path = self._item.path.parent / image_path

            if not image_path.is_file():
                raise FileDoesNotExistError(image_path)

            if image_path.suffix.lower() not in SUPPORTED_TYPES:
                raise ImageTypeNotSupportedError(image_path.suffix)
