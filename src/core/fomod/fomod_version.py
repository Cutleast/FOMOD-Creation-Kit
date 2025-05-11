"""
Copyright (c) Cutleast
"""

from typing import Optional

from pydantic_xml import BaseXmlModel, attr


class FomodVersion(BaseXmlModel):
    """
    Model representing the Version tag of the info.xml.
    """

    version: str = ""
    """The version of the mod."""

    machine_version: Optional[str] = attr(name="MachineVersion", default=None)
    """A machine-readable representation of the version."""
