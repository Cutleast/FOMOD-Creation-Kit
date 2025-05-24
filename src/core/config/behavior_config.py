"""
Copyright (c) Cutleast
"""

from enum import Enum
from typing import override

from .base_config import BaseConfig


class BehaviorConfig(BaseConfig):
    """
    Class for managing behavior settings.
    """

    finalize_on_save: bool = True
    """Whether to finalize the FOMOD installer when saving it."""

    validate_xml_on_save: bool = False
    """Whether to validate the XML files when saving a FOMOD installer."""

    class ModuleConfigEncoding(Enum):
        """Enum for valid encodings for the ModuleConfig.xml file."""

        UTF8 = "utf-8"
        """Standard UTF-8 encoding."""

        UTF16LE = "utf-16le"
        """Little-endian UTF-16 encoding."""

    module_config_encoding: ModuleConfigEncoding = ModuleConfigEncoding.UTF8
    """Encoding used when saving the ModuleConfig.xml file."""

    @override
    @staticmethod
    def get_config_name() -> str:
        return "behavior.json"
