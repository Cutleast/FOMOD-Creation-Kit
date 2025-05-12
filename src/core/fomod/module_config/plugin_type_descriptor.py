"""
Copyright (c) Cutleast
"""

from typing import Optional

from pydantic_xml import BaseXmlModel, element

from .dependency.dependency_plugin_type import DependencyPluginType
from .plugin_type import PluginType


class PluginTypeDescriptor(BaseXmlModel, search_mode="unordered"):
    """
    Model representing a plugin type descriptor.
    """

    dependency_type: Optional[DependencyPluginType] = element(
        name="dependencyType", default=None
    )
    """
    Used when the plugin type is dependent upon the state of other mods.
    Mutual exclusive with `type`.
    """

    type: Optional[PluginType] = element(name="type", default=None)
    """The type of the plugin. Mutual exclusive with `dependency_type`."""
