"""
Copyright (c) Cutleast
"""

from ..plugin.plugin_type import PluginType


class DefaultPluginType(PluginType, tag="defaultType"):
    """
    Model representing the default plugin type of a dependency type.
    """

    # I don't know why but this extra class is required for the "defaultType" tag to work
