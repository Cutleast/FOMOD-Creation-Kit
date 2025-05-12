"""
Copyright (c) Cutleast
"""

from pydantic_xml import BaseXmlModel, element

from .dependency_pattern import DependencyPattern


class DependencyPatternList(BaseXmlModel):
    """
    Model representing a list of dependency patterns.
    """

    patterns: list[DependencyPattern] = element(tag="pattern")
    """
    A list of specific patterns of mod files and condition flags against which to match
    the user's installation.
    """
