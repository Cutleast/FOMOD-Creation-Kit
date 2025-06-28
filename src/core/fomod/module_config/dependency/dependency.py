"""
Copyright (c) Cutleast
"""

from pydantic_xml import BaseXmlModel


class Dependency(BaseXmlModel, search_mode="unordered"):
    """
    Base model for dependencies.
    """

    def get_display_name(self) -> str:
        """
        Returns:
            str: A display name generated from the dependency.
        """

        return str(self)
