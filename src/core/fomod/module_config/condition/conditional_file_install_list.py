"""
Copyright (c) Cutleast
"""

from pydantic_xml import BaseXmlModel, element

from .conditional_install_pattern_list import ConditionalInstallPatternList


class ConditionalFileInstallList(BaseXmlModel):
    """
    Model representing a list of optional files that may optionally be installed for this
    module, based on condition flags.
    """

    patterns: ConditionalInstallPatternList = element(tag="patterns")
    """
    The list of patterns against which to match the conditional flags and installed
    files. All matching patterns will have their files installed.
    """
