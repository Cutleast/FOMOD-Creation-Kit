"""
Copyright (c) Cutleast
"""

from pydantic_xml import BaseXmlModel, element

from .default_plugin_type import DefaultPluginType
from .dependency_pattern_list import DependencyPatternList


class DependencyPluginType(BaseXmlModel, tag="dependencyType", search_mode="unordered"):
    """
    Model representing a plugin type that is dependent upon the state of other mods.
    """

    default_type: DefaultPluginType = element(name="defaultType")
    """
    The default type of the plugin used if none of the specified dependency states are
    satisfied.
    """

    patterns: DependencyPatternList = element(name="patterns")
    """
    The list of dependency patterns against which to match the user's installation. The
    first pattern that matches the user's installation determines the type of the plugin.
    """
