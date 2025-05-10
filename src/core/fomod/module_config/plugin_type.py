"""
Copyright (c) Cutleast
"""

from enum import Enum

from pydantic_xml import BaseXmlModel, attr


class PluginType(BaseXmlModel):
    """
    Model representing the type of a given plugin.
    """

    class PluginTypeEnum(Enum):
        """
        Enum for the possible plugin types.
        """

        Required = "Required"
        """Indicates the plugin must be installed."""

        Optional = "Optional"
        """Indicates the plugin is optional."""

        Recommended = "Recommended"
        """Indicates the plugin is recommended for stability."""

        NotUsable = "NotUsable"
        """
        Indicates that using the plugin could result in instability (i.e., a prerequisite
        plugin is missing).
        """

        CouldBeUsable = "CouldBeUsable"
        """
        Indicates that using the plugin could result in instability if loaded with the
        currently active plugins (i.e., a prerequisite plugin is missing), but that the
        prerequisite plugin is installed, just not activated.
        """

    name: PluginTypeEnum = attr(name="name")
    """The name of the plugin type."""
