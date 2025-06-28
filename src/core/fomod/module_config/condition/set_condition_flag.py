"""
Copyright (c) Cutleast
"""

from typing import override

from pydantic_xml import BaseXmlModel, attr


class SetConditionFlag(BaseXmlModel):
    """
    Model representing a condition flag to set if a plugin is selected.
    """

    value: str
    """The value of the condition flag."""

    name: str = attr(name="name")
    """The identifying name of the condition flag."""

    @override
    def __str__(self) -> str:
        return f"{self.name}={self.value}"
