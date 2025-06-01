"""
Copyright (c) Cutleast
"""

from __future__ import annotations

from pydantic_xml import BaseXmlModel, element

from ..plugin.plugin_type import PluginType
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

    @staticmethod
    def create() -> DependencyPattern:
        """
        Creates a dependency pattern with the bare minimum.

        Returns:
            DependencyPattern: The new dependency pattern
        """

        return DependencyPattern(
            dependencies=CompositeDependency(),
            type=PluginType(name=PluginType.Type.Recommended),
        )
