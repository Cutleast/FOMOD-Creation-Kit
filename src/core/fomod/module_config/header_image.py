"""
Copyright (c) Cutleast
"""

from pathlib import Path
from typing import Optional

from pydantic_xml import BaseXmlModel, attr


class HeaderImage(BaseXmlModel, search_mode="unordered"):
    """
    Model representing the headerImage tag of the ModuleConfig.xml.

    An image.
    """

    path: Optional[Path] = attr(name="path", default=None)
    """The path to the image in the FOMOD. If omitted the FOMOD's screenshot is used."""

    show_image: bool = attr(name="showImage", default=True)
    """Whether or not the image should be displayed."""

    show_fade: bool = attr(name="showFade", default=True)
    """
    Whether or not the fade effect should be displayed.
    This value is ignored if showImage is false.
    """

    height: int = attr(name="height", default=-1)
    """
    The height to use for the image.
    Note that there is a minimum height that is enforced based on the user's settings.
    """
