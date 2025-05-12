"""
Copyright (c) Cutleast
"""

from pydantic_xml import BaseXmlModel, element

from .conditional_install_pattern import ConditionalInstallPattern


class ConditionalInstallPatternList(BaseXmlModel):
    """
    Model representing a list of conditional install patterns.
    """

    patterns: list[ConditionalInstallPattern] = element(
        tag="pattern", default_factory=list
    )
    """
    A specific pattern of mod files and condition flags against which to match the user's
    installation.
    """
