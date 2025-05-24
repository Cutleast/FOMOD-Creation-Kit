"""
Copyright (c) Cutleast
"""

from pathlib import Path
from typing import Optional

from pydantic_xml import BaseXmlModel, attr


class FileSystemItem(BaseXmlModel, search_mode="unordered"):
    """
    Model representing the fileSystemItem tag of the ModuleConfig.xml.

    A file or folder that may be installed as part of a module or plugin.
    """

    source: Path = attr(name="source")
    """The path to the file or folder in the FOMOD."""

    destination: Optional[Path] = attr(name="destination", default=None)
    """
    The path to which the file or folder should be installed. If omitted, the 
    destination is the same as the source.
    """

    always_install: bool = attr(name="alwaysInstall", default=False)
    """
    Indicates that the file or folder should always be installed, regardless 
    of whether or not the plugin has been selected.
    """

    install_if_usable: bool = attr(name="installIfUsable", default=False)
    """
    Indicates that the file or folder should always be installed if the plugin 
    is not NotUsable, regardless of whether or not the plugin has been selected.
    """

    priority: int = attr(name="priority", default=0)
    """
    A number describing the relative priority of the file or folder. A higher 
    number indicates the file or folder should be installed after the items 
    with lower numbers. This value does not have to be unique.
    """
