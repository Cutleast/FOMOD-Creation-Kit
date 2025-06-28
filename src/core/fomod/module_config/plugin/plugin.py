"""
Copyright (c) Cutleast
"""

from __future__ import annotations

from typing import Optional, Self, override

from pydantic import model_validator
from pydantic_xml import BaseXmlModel, attr, element
from PySide6.QtWidgets import QApplication

from ..condition.condition_flag_list import ConditionFlagList
from ..file_system.file_list import FileList
from ..image import Image
from .plugin_type import PluginType
from .plugin_type_descriptor import PluginTypeDescriptor


class Plugin(BaseXmlModel, search_mode="unordered"):
    """
    Model representing a plugin.
    """

    name: str = attr(name="name")
    """The name of the plugin."""

    description: str = element(tag="description", default="")
    """The description of the plugin."""

    image: Optional[Image] = element(tag="image", default=None)
    """The optional image associated with the plugin."""

    files: Optional[FileList] = element(tag="files", default=None)
    """The list of files and folders that need to be installed for the plugin."""

    condition_flags: Optional[ConditionFlagList] = element(
        tag="conditionFlags", default=None
    )
    """The list of condition flags to set if the plugin is in the appropriate state."""

    type_descriptor: PluginTypeDescriptor = element(tag="typeDescriptor")
    """Describes the type of the plugin."""

    @model_validator(mode="after")
    def create_missing_description(self) -> Self:
        """
        Creates a description from the name if one is not provided.

        Returns:
            Self: The plugin.
        """

        if not self.description:
            self.description = self.name

        return self

    @override
    def __str__(self) -> str:
        return self.name or "<" + QApplication.translate("Plugin", "unnamed") + ">"

    @staticmethod
    def create() -> Plugin:
        """
        Creates a plugin with the bare minimum.

        Returns:
            Plugin: The new plugin
        """

        return Plugin(
            name="",
            type_descriptor=PluginTypeDescriptor(
                type=PluginType(name=PluginType.Type.Optional)
            ),
        )
