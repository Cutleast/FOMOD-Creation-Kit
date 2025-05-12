"""
Copyright (c) Cutleast
"""

from pydantic_xml import BaseXmlModel, attr, element

from .dependency.composite_dependency import CompositeDependency
from .group_list import GroupList


class InstallStep(BaseXmlModel, tag="installStep", search_mode="unordered"):
    """
    Model representing the installStep tag of the ModuleConfig.xml.

    A step in the install process containing groups of optional plugins.
    """

    name: str = attr(name="name")
    """The name of the install step."""

    visible: list[CompositeDependency] = element(tag="visible", default_factory=list)
    """
    The pattern against which to match the conditional flags and installed files. If the 
    pattern is matched, then the install step will be visible.
    """

    optional_file_groups: GroupList = element(tag="optionalFileGroups")
    """
    The list of optional files (or plugins) that may optionally be installed for this
    module.
    """
