"""
Copyright (c) Cutleast
"""

from pydantic_xml import BaseXmlModel


class Dependency(BaseXmlModel, search_mode="unordered"):
    """
    Base model for dependencies.
    """
