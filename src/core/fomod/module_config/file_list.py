"""
Copyright (c) Cutleast
"""

from pydantic_xml import BaseXmlModel, element

from .file_item import FileItem
from .folder_item import FolderItem


class FileList(BaseXmlModel, search_mode="unordered"):
    """
    Model representing the fileList tag of the ModuleConfig.xml.

    A list of files and folders.
    """

    files: list[FileItem] = element(tag="file", default_factory=list)
    """Files belonging to the plugin or module."""

    folders: list[FolderItem] = element(tag="folder", default_factory=list)
    """Folders belonging to the plugin or module."""
