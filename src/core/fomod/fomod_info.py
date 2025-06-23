"""
Copyright (c) Cutleast
"""

from __future__ import annotations

from typing import Optional, override

from pydantic_xml import element

from .fomod_model import FomodModel
from .fomod_version import FomodVersion


class FomodInfo(FomodModel, tag="fomod", search_mode="unordered"):
    """
    Model representing the info.xml file of a FOMOD installer.
    """

    name: str = element(tag="Name", default="")
    """The name of the mod."""

    author: str = element(tag="Author", default="")
    """The author of the mod."""

    version: Optional[FomodVersion] = element(tag="Version", default=None)
    """The version of the mod."""

    website: str = element(tag="Website", default="")
    """The website of the mod."""

    description: str = element(tag="Description", default="")
    """The description of the mod."""

    id: str = element(tag="Id", default="")
    """The id of the mod."""

    @override
    @classmethod
    def get_schema_url(cls) -> str:
        return "https://raw.githubusercontent.com/Cutleast/FOMOD-Creation-Kit/master/res/schemas/info.xsd"
