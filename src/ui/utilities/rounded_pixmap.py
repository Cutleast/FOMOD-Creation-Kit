"""
Copyright (c) Cutleast
"""

from PySide6.QtCore import QRectF, Qt
from PySide6.QtGui import QPainter, QPainterPath, QPixmap


def rounded_pixmap(pixmap: QPixmap, radius: int = 5) -> QPixmap:
    """
    Adds rounded corners to a pixmap with a specified radius in pixels.

    Args:
        pixmap (QPixmap): Pixmap to add rounded corners to.
        radius (int, optional): Radius in pixels. Defaults to 5.

    Returns:
        QPixmap: Pixmap with rounded corners
    """

    size = pixmap.size()
    rounded = QPixmap(size)
    rounded.fill(Qt.GlobalColor.transparent)

    painter = QPainter(rounded)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    path = QPainterPath()
    path.addRoundedRect(QRectF(0, 0, size.width(), size.height()), radius, radius)
    painter.setClipPath(path)
    painter.drawPixmap(0, 0, pixmap)
    painter.end()

    return rounded
