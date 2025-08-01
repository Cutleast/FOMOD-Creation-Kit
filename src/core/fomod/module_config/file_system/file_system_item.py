"""
Copyright (c) Cutleast
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, override

from pydantic import field_serializer
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

    @override
    def __str__(self) -> str:
        if self.destination is not None:
            return f"'{self.source}' → '{self.destination}'"
        else:
            return f"'{self.source}'"

    @classmethod
    def create[T: FileSystemItem](cls: type[T]) -> T:
        """
        Creates a file system item with the bare minimum.

        Returns:
            T: The new file system item
        """

        return cls(source=Path("__default__"))

    @field_serializer("source", "destination")
    def serialize_path(self, path: Optional[Path]) -> Optional[Path | str]:
        if path == Path():
            return ""

        return path
