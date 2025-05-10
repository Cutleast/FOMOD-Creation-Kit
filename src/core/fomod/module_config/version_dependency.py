"""
Copyright (c) Cutleast
"""

from pydantic_xml import BaseXmlModel, attr


class VersionDependency(BaseXmlModel):
    """
    Model representing a required minimum version of an item.
    """

    version: str = attr(name="version")
    """The required minimum version of the item."""
