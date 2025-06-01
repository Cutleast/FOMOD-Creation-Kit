"""
Copyright (c) Cutleast
"""

from __future__ import annotations

from typing import Optional, override

from pydantic_xml import BaseXmlModel, attr, element
from PySide6.QtWidgets import QApplication

from .group_list import GroupList
from .visible import Visible


class InstallStep(BaseXmlModel, search_mode="unordered"):
    """
    Model representing the installStep tag of the ModuleConfig.xml.

    A step in the install process containing groups of optional plugins.
    """

    name: str = attr(name="name")
    """The name of the install step."""

    visible: Optional[Visible] = element(tag="visible", default=None)
    """
    The pattern against which to match the conditional flags and installed files. If the 
    pattern is matched, then the install step will be visible.
    """

    optional_file_groups: GroupList = element(tag="optionalFileGroups")
    """
    The list of optional files (or plugins) that may optionally be installed for this
    module.
    """

    @override
    def __str__(self) -> str:
        return self.name or "<" + QApplication.translate("InstallStep", "unnamed") + ">"

    @staticmethod
    def create() -> InstallStep:
        """
        Creates a new InstallStep with the bare minimum.

        Returns:
            InstallStep: The new install step
        """

        return InstallStep(name="", optional_file_groups=GroupList(groups=[]))
