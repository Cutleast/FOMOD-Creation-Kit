"""
Copyright (c) Cutleast
"""

from enum import Enum

from pydantic_xml import BaseXmlModel, attr


class FileDependency(BaseXmlModel, search_mode="unordered"):
    """
    Model representing the fileDependency tag of the ModuleConfig.xml.

    A mod upon which the type of a plugin depends.
    """

    file: str = attr(name="file")
    """The file of the mod upon which a plugin depends."""

    class State(Enum):
        """
        Enum for the states of a mod file.
        """

        Missing = "Missing"
        """Indicates the mod file is not installed."""

        Inactive = "Inactive"
        """Indicates the mod file is installed, but not active."""

        Active = "Active"
        """Indicates the mod file is installed and active."""

    state: State = attr(name="state")
    """The state of the mod file."""
