"""
Copyright (c) Cutleast
"""

from typing import Optional

from pydantic_xml import BaseXmlModel, attr, element

from .condition.condition_flag_list import ConditionFlagList
from .file_list import FileList
from .image import Image
from .plugin_type_descriptor import PluginTypeDescriptor


class Plugin(BaseXmlModel, tag="plugin", search_mode="unordered"):
    """
    Model representing a plugin.
    """

    name: str = attr(name="name")
    """The name of the plugin."""

    description: str = element(name="description", default="")
    """The description of the plugin."""

    image: Optional[Image] = element(name="image", default=None)
    """The optional image associated with the plugin."""

    files: Optional[FileList] = element(tag="files", default=None)
    """The list of files and folders that need to be installed for the plugin."""

    condition_flags: Optional[ConditionFlagList] = element(
        tag="conditionFlags", default=None
    )
    """The list of condition flags to set if the plugin is in the appropriate state."""

    type_descriptor: PluginTypeDescriptor = element(tag="typeDescriptor")
    """Describes the type of the plugin."""
