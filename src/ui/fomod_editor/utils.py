"""
Copyright (c) Cutleast
"""

from pathlib import Path
from typing import Optional

import qtawesome as qta
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap

from core.fomod.module_config.plugin.plugin import Plugin
from core.utilities.path import get_joined_path_if_relative
from ui.utilities.rounded_pixmap import rounded_pixmap
from ui.utilities.tool_tip import pixmap_to_html


class Utils:
    """
    Class with static utility methods to be used by the FOMOD editor widgets.
    """

    @staticmethod
    def create_tooltip_text_for_plugin(
        plugin: Plugin, fomod_path: Optional[Path] = None, image_size: int = 256
    ) -> str:
        """
        Creates the tooltip text for a plugin.

        Args:
            plugin (Plugin): The plugin to create the tooltip text for.
            fomod_path (Optional[Path], optional): The path to the fomod. Defaults to None.

        Returns:
            str: The tooltip text.
        """

        html_text: str = ""

        pixmap: QPixmap
        if (
            plugin.image is not None
            and (
                image_path := get_joined_path_if_relative(
                    plugin.image.path,
                    fomod_path.parent if fomod_path is not None else None,
                )
            ).is_file()
        ):
            pixmap = rounded_pixmap(
                QPixmap(str(image_path)).scaledToHeight(
                    image_size,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        else:
            pixmap = qta.icon("mdi6.image-off-outline", color="#666666").pixmap(
                image_size, image_size
            )

        html_text: str = f"""
<center>{pixmap_to_html(pixmap)}</center>
<br>
{plugin.get_summary().replace("\n", "<br>")}
"""

        return html_text
