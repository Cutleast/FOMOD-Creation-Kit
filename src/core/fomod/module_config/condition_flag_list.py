"""
Copyright (c) Cutleast
"""

from pydantic_xml import BaseXmlModel, element

from .set_condition_flag import SetConditionFlag


class ConditionFlagList(BaseXmlModel):
    """
    Model representing a list of condition flags to set if a plugin is in the
    appropriate state.
    """

    flags: list[SetConditionFlag] = element(tag="flag")
    """List of condition flags to set if the plugin is selected."""
