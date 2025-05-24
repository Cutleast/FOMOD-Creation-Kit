"""
Copyright (c) Cutleast
"""

from pathlib import Path

from pydantic_xml import BaseXmlModel, attr


class Image(BaseXmlModel):
    """
    Model representing an image.
    """

    path: Path = attr(name="path")
    """The path to the image in the mod."""
