"""
Copyright (c) Cutleast
"""

from pydantic_xml import BaseXmlModel, element

from .file_system_item import FileSystemItem


class FileList(BaseXmlModel, search_mode="unordered"):
    """
    Model representing the fileList tag of the ModuleConfig.xml.

    A list of files and folders.
    """

    files: list[FileSystemItem] = element(tag="file", default_factory=list)
    """Files belonging to the plugin or module."""

    folders: list[FileSystemItem] = element(tag="folder", default_factory=list)
    """Folders belonging to the plugin or module."""
