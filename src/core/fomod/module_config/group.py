"""
Copyright (c) Cutleast
"""

from enum import Enum

from pydantic_xml import BaseXmlModel, attr, element

from .plugin_list import PluginList


class Group(BaseXmlModel, tag="group", search_mode="unordered"):
    """
    Model representing a group of plugins.
    """

    name: str = attr(name="name")
    """The name of the group."""

    plugins: PluginList = element(tag="plugins")
    """The list of plugins in the group."""

    class Type(Enum):
        """
        Enum for possible group types.
        """

        SelectAtLeastOne = "SelectAtLeastOne"
        """At least one plugin in the group must be selected."""

        SelectAtMostOne = "SelectAtMostOne"
        """At most one plugin in the group must be selected."""

        SelectExactlyOne = "SelectExactlyOne"
        """Exactly one plugin in the group must be selected."""

        SelectAll = "SelectAll"
        """All plugins in the group must be selected."""

        SelectAny = "SelectAny"
        """Any number of plugins in the group may be selected."""

    type: Type = attr(name="type")
    """The type of the group."""
