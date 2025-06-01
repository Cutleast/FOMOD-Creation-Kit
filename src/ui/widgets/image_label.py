"""
Copyright (c) Cutleast
"""

from typing import override

from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QMouseEvent, QPixmap, QResizeEvent
from PySide6.QtWidgets import QLabel

from ui.widgets.image_viewer import ImageViewer

from ..utilities.rounded_pixmap import rounded_pixmap


class ImageLabel(QLabel):
    """
    QLabel adapted to display images that automatically resize dynamically to the label
    size.
    """

    __round_pixmap: bool
    __enable_viewer: bool
    __current_pixmap: QPixmap

    def __init__(
        self, pixmap: QPixmap, round_pixmap: bool = False, enable_viewer: bool = True
    ) -> None:
        """
        Args:
            pixmap (QPixmap): Initial pixmap to display
            round_pixmap (bool, optional):
                Whether to display the image with rounded corners by adding a transparent
                mask. Defaults to False.
            enable_viewer (bool, optional):
                Whether to open the image in a separate window when double-clicked.
                Defaults to True.
        """

        super().__init__()

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.__round_pixmap = round_pixmap
        self.__enable_viewer = enable_viewer

        self.setPixmap(pixmap)

    @override
    def setPixmap(self, pixmap: QPixmap | QImage) -> None:
        if isinstance(pixmap, QImage):
            pixmap = QPixmap(pixmap)

        self.__current_pixmap = pixmap
        self.__update_image()

    @override
    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)

        self.__update_image()

    def __update_image(self) -> None:
        scaled_pixmap: QPixmap = self.__current_pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )

        if self.__round_pixmap:
            scaled_pixmap = rounded_pixmap(scaled_pixmap)

        super().setPixmap(scaled_pixmap)

    @override
    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        super().mouseDoubleClickEvent(event)

        if self.__enable_viewer:
            self.__open_in_viewer()

    def __open_in_viewer(self) -> None:
        viewer = ImageViewer(self.__current_pixmap, self)
        viewer.setWindowFlag(Qt.WindowType.Window, True)
        viewer.show()
