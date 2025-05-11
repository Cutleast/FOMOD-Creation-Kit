"""
Copyright (c) Cutleast
"""

from pathlib import Path
from typing import Optional, override

import qtawesome as qta
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QFileDialog,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPlainTextEdit,
)

from core.fomod.fomod import Fomod
from core.fomod.module_config.header_image import SUPPORTED_TYPES, HeaderImage
from core.fomod_editor.exceptions import (
    FileDoesNotExistError,
    ImageTypeNotSupportedError,
    PathNotInFomodError,
)
from ui.utilities.rounded_pixmap import rounded_pixmap
from ui.widgets.browse_edit import BrowseLineEdit
from ui.widgets.url_edit import UrlEdit

from .base_editor_widget import BaseEditorWidget


class InfoEditorWidget(BaseEditorWidget):
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
    __description_entry: QPlainTextEdit
    __image_path_entry: BrowseLineEdit
    __image_label: QLabel

    def __init__(self, fomod: Fomod) -> None:
        super().__init__(fomod)

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
            self._fomod.module_config.header_image is not None
            and self._fomod.module_config.header_image.path is not None
            and self._fomod.path is not None
        ):
            image_path: Path = (
                self._fomod.path.parent / self._fomod.module_config.header_image.path
            )
            self.__image_path_entry.setText(str(image_path))

    @override
    def _init_ui(self) -> None:
        super()._init_ui()

        self.__flayout = QFormLayout()
        self._vlayout.addLayout(self.__flayout)

        self.__init_form()

    def __init_form(self) -> None:
        self.__image_label = QLabel()
        self.__image_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.__image_label.setFixedHeight(InfoEditorWidget.IMAGE_HEIGHT)
        self.__image_label.setPixmap(
            qta.icon("mdi6.image-off-outline", color="#666666").pixmap(
                InfoEditorWidget.IMAGE_HEIGHT, InfoEditorWidget.IMAGE_HEIGHT
            )
        )
        self.__flayout.addRow(self.__image_label)

        self.__name_entry = QLineEdit()
        self.__name_entry.setText(self._fomod.info.name)
        self.__flayout.addRow(self.tr("Name:"), self.__name_entry)

        self.__author_entry = QLineEdit()
        self.__author_entry.setText(self._fomod.info.author)
        self.__flayout.addRow(self.tr("Author:"), self.__author_entry)

        self.__version_entry = QLineEdit()
        self.__version_entry.setText(self._fomod.info.version.version)
        self.__flayout.addRow(self.tr("Version:"), self.__version_entry)

        self.__website_entry = UrlEdit()
        self.__website_entry.setText(self._fomod.info.website)
        self.__flayout.addRow(self.tr("Website:"), self.__website_entry)

        self.__description_entry = QPlainTextEdit()
        self.__description_entry.setPlainText(self._fomod.info.description)
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

        if image_path is not None and image_path.is_file():
            self.__image_label.setPixmap(
                rounded_pixmap(
                    QPixmap(str(image_path)).scaledToHeight(
                        InfoEditorWidget.IMAGE_HEIGHT,
                        mode=Qt.TransformationMode.SmoothTransformation,
                    )
                )
            )
        else:
            self.__image_label.setPixmap(
                qta.icon("mdi6.image-off-outline", color="#666666").pixmap(
                    InfoEditorWidget.IMAGE_HEIGHT, InfoEditorWidget.IMAGE_HEIGHT
                )
            )

    @override
    def save(self) -> None:
        self._fomod.info.name = self.__name_entry.text()
        self._fomod.module_config.module_name.title = self.__name_entry.text()
        self._fomod.info.author = self.__author_entry.text()
        self._fomod.info.version.version = self.__version_entry.text()
        self._fomod.info.website = self.__website_entry.text()
        self._fomod.info.description = self.__description_entry.toPlainText()

        image_path: Optional[Path] = (
            Path(self.__image_path_entry.text().strip())
            if self.__image_path_entry.text().strip()
            else None
        )
        if image_path is not None and self._fomod.path is not None:
            if self._fomod.module_config.header_image is None:
                self._fomod.module_config.header_image = HeaderImage()
            self._fomod.module_config.header_image.path = image_path.relative_to(
                self._fomod.path.parent
            )
        else:
            self._fomod.module_config.header_image = None

    @override
    def validate(self) -> None:
        image_path: Optional[Path] = (
            Path(self.__image_path_entry.text().strip())
            if self.__image_path_entry.text().strip()
            else None
        )

        if image_path is not None:
            if self._fomod.path is None:
                raise ValueError(self.tr("No FOMOD path is set!"))

            if not image_path.is_file():
                raise FileDoesNotExistError(image_path)

            if not image_path.is_relative_to(self._fomod.path.parent):
                raise PathNotInFomodError(image_path, self._fomod.path.parent)

            if image_path.suffix.lower() not in SUPPORTED_TYPES:
                raise ImageTypeNotSupportedError(image_path.suffix)
