"""
Copyright (c) Cutleast
"""

from typing import Optional, override

from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPainter, QPixmap, QWheelEvent
from PySide6.QtWidgets import QGraphicsItem, QGraphicsScene, QGraphicsView, QWidget


class ImageViewer(QGraphicsView):
    """
    Widget for displaying an image that supports zooming and dragging with the mouse.
    """

    MAX_SIZE: int = 1_000
    """Maximum preset size when opening the image."""

    TITLEBAR_HEIGHT: int = 44
    """The height of the Windows title bar in pixels."""

    __graphics_item: QGraphicsItem

    def __init__(
        self, image: QImage | QPixmap, parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(parent)

        self.setWindowTitle(f"{image.width()}x{image.height()}")
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

        scene = QGraphicsScene()
        self.__graphics_item = scene.addPixmap(image)
        self.__graphics_item.setTransformationMode(
            Qt.TransformationMode.SmoothTransformation
        )
        self.setScene(scene)

        width: int = min(ImageViewer.MAX_SIZE, image.width())
        self.resize(
            width, image.scaledToWidth(width).height() + ImageViewer.TITLEBAR_HEIGHT
        )

    # TODO: Auto resize image when the window is resized but this prevents zooming in
    # @override
    # def resizeEvent(self, event: QResizeEvent) -> None:
    #     super().resizeEvent(event)

    #     self.fitInView(self.__graphics_item, Qt.AspectRatioMode.KeepAspectRatio)

    @override
    def wheelEvent(self, event: QWheelEvent) -> None:
        modifiers: Qt.KeyboardModifier = event.modifiers()

        if modifiers == Qt.KeyboardModifier.ControlModifier:
            if event.angleDelta().y() > 0:
                self.scale(1.1, 1.1)
            else:
                self.scale(0.9, 0.9)

        else:
            super().wheelEvent(event)
