"""
Copyright (c) Cutleast
"""

from enum import Enum

from pydantic_xml import BaseXmlModel, attr


class ModuleTitle(BaseXmlModel):
    """
    Model representing the moduleTitle tag of the ModuleConfig.xml.

    Describes the display properties of the module title.
    """

    title: str = ""
    """The title of the module."""

    class Position(Enum):
        """Enum for the possible positions of the title."""

        Left = "Left"
        """Positions the title on the left side of the form header."""

        Right = "Right"
        """Positions the title on the right side of the form header."""

        RightOfImage = "RightOfImage"
        """Positions the title on the right side of the image in the form header."""

    position: Position = attr(name="position", default=Position.Left)
    """Title position."""

    color: str = attr(name="colour", default="000000")
    """The color to use for the title."""
