"""
Copyright (c) Cutleast
"""

from typing import override

from pydantic_xml import BaseXmlModel, attr
from PySide6.QtWidgets import QApplication

from core.utilities.localized_enum import LocalizedEnum


class PluginType(BaseXmlModel):
    """
    Model representing the type of a given plugin.
    """

    class Type(LocalizedEnum):
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

        @override
        def get_localized_name(self) -> str:
            locs: dict[PluginType.Type, str] = {
                PluginType.Type.Required: QApplication.translate(
                    "PluginType", "Required"
                ),
                PluginType.Type.Optional: QApplication.translate(
                    "PluginType", "Optional"
                ),
                PluginType.Type.Recommended: QApplication.translate(
                    "PluginType", "Recommended"
                ),
                PluginType.Type.NotUsable: QApplication.translate(
                    "PluginType", "Not usable"
                ),
                PluginType.Type.CouldBeUsable: QApplication.translate(
                    "PluginType", "Could be usable"
                ),
            }

            return locs[self]

        @override
        def get_localized_description(self) -> str:
            locs: dict[PluginType.Type, str] = {
                PluginType.Type.Required: QApplication.translate(
                    "PluginType", "The plugin must be installed."
                ),
                PluginType.Type.Optional: QApplication.translate(
                    "PluginType", "The plugin is optional."
                ),
                PluginType.Type.Recommended: QApplication.translate(
                    "PluginType", "The plugin is recommended for stability."
                ),
                PluginType.Type.NotUsable: QApplication.translate(
                    "PluginType",
                    "Using the plugin could result in instability (i.e., a prerequisite "
                    "plugin is missing).",
                ),
                PluginType.Type.CouldBeUsable: QApplication.translate(
                    "PluginType",
                    "Using the plugin could result in instability if loaded with the "
                    "currently active plugins (i.e., a prerequisite plugin is missing), "
                    "but that the prerequisite plugin is installed, just not activated.",
                ),
            }

            return locs[self]

    name: Type = attr(name="name")
    """The name of the plugin type."""

    @override
    def __str__(self) -> str:
        return self.name.get_localized_name()
