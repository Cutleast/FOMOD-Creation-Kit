"""
Copyright (c) Cutleast
"""

from pydantic_xml import BaseXmlModel, element

from ..plugin_type import PluginType
from .composite_dependency import CompositeDependency


class DependencyPattern(BaseXmlModel, search_mode="unordered"):
    """
    Model representing a pattern of mod files and condition flags that determine the
    type of a plugin.
    """

    dependencies: CompositeDependency = element(tag="dependencies")
    """
    The list of mods and their states against which to match the user's installation.
    """

    type: PluginType = element(tag="type")
    """The type of the plugin."""
