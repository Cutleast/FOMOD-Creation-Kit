"""
Copyright (c) Cutleast
"""

from PySide6.QtCore import QBuffer, QIODevice, Qt
from PySide6.QtGui import QPixmap


def pixmap_to_html(pixmap: QPixmap, image_size: int = 200) -> str:
    """
    Creates an HTML image tag from a pixmap, suited for tool tips.

    Args:
        pixmap (QPixmap): Pixmap to create HTML image tag from

    Returns:
        str: HTML image tag
    """

    buffer = QBuffer()
    buffer.open(QIODevice.OpenModeFlag.WriteOnly)
    pixmap.scaled(
        image_size,
        image_size,
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation,
    ).save(buffer, "PNG", quality=100)
    image: str = bytes(buffer.data().toBase64().data()).decode()
    html_text: str = f'<img src="data:image/png;base64,{image}">'

    return html_text
