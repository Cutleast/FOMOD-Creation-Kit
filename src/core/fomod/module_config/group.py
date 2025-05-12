"""
Copyright (c) Cutleast
"""

from typing import override

from pydantic_xml import BaseXmlModel, attr, element
from PySide6.QtWidgets import QApplication

from core.utilities.localized_enum import LocalizedEnum

from .plugin_list import PluginList


class Group(BaseXmlModel, tag="group", search_mode="unordered"):
    """
    Model representing a group of plugins.
    """

    name: str = attr(name="name")
    """The name of the group."""

    plugins: PluginList = element(tag="plugins")
    """The list of plugins in the group."""

    class Type(LocalizedEnum):
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

        @override
        def get_localized_name(self) -> str:
            locs: dict[Group.Type, str] = {
                Group.Type.SelectAtLeastOne: QApplication.translate(
                    "Group", "Select at least one"
                ),
                Group.Type.SelectAtMostOne: QApplication.translate(
                    "Group", "Select at most one"
                ),
                Group.Type.SelectExactlyOne: QApplication.translate(
                    "Group", "Select exactly one"
                ),
                Group.Type.SelectAll: QApplication.translate("Group", "Select all"),
                Group.Type.SelectAny: QApplication.translate("Group", "Select any"),
            }

            return locs[self]

        @override
        def get_localized_description(self) -> str:
            locs: dict[Group.Type, str] = {
                Group.Type.SelectAtLeastOne: QApplication.translate(
                    "Group",
                    "At least one plugin in the group must be selected.",
                ),
                Group.Type.SelectAtMostOne: QApplication.translate(
                    "Group",
                    "At most one plugin in the group must be selected.",
                ),
                Group.Type.SelectExactlyOne: QApplication.translate(
                    "Group",
                    "Exactly one plugin in the group must be selected.",
                ),
                Group.Type.SelectAll: QApplication.translate(
                    "Group",
                    "All plugins in the group must be selected.",
                ),
                Group.Type.SelectAny: QApplication.translate(
                    "Group",
                    "Any number of plugins in the group may be selected.",
                ),
            }

            return locs[self]

    type: Type = attr(name="type")
    """The type of the group."""
