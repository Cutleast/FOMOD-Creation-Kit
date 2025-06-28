"""
Copyright (c) Cutleast
"""

from typing import override

from pydantic_xml import attr

from .dependency import Dependency


class FlagDependency(Dependency):
    """
    A condition flag upon which the type of a plugin depends.
    """

    flag: str = attr(name="flag")
    """The name of the condition flag upon which a the plugin depends."""

    value: str = attr(name="value")
    """The value of the condition flag upon which a the plugin depends."""

    @override
    def __str__(self) -> str:
        return f"{self.flag}={self.value}"
