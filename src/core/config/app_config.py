"""
Copyright (c) Cutleast
"""

from cutleast_core_lib.core.config.app_config import AppConfig as BaseAppConfig
from cutleast_core_lib.core.utilities.base_enum import BaseEnum
from cutleast_core_lib.core.utilities.dynamic_default_model import default_factory


class AppConfig(BaseAppConfig):
    """
    Class for managing application settings.
    """

    class AppLanguage(BaseEnum):
        """Enum for the languages supported by the app."""

        System = "System"
        German = "de_DE"
        English = "en_US"
        Portuguese = "pt_BR"

    language: AppLanguage = AppLanguage.System

    @default_factory("log_visible")
    @classmethod
    def get_default_log_visible(cls) -> bool:
        """
        Returns:
            str: Default value for log_visible.
        """

        return False  # hide log by default

    @default_factory("accent_color")
    @classmethod
    def get_default_accent_color(cls) -> str:
        """
        Returns:
            str: Default accent color.
        """

        return "#ff5b51"
