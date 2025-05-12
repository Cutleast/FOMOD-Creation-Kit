"""
Copyright (c) Cutleast
"""

from pydantic_xml import BaseXmlModel, element

from ..dependency.composite_dependency import CompositeDependency
from ..file_list import FileList


class ConditionalInstallPattern(
    BaseXmlModel, tag="conditionalInstallPattern", search_mode="unordered"
):
    """
    Model representing a pattern of mod files and conditional flags that determine
    whether to install specific files.
    """

    dependencies: list[CompositeDependency] = element(tag="dependencies")
    """The list of mods and their states against which to match the user's installation."""

    files: FileList = element(tag="files")
    """The files and folders to install if the pattern is matched."""
