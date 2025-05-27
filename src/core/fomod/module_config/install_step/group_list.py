"""
Copyright (c) Cutleast
"""

from pydantic_xml import BaseXmlModel, attr, element

from .group import Group
from .order import Order


class GroupList(BaseXmlModel):
    """
    Model representing a list of plugin groups.
    """

    groups: list[Group] = element(tag="group")
    """A group of plugins for the mod."""

    order: Order = attr(name="order", default=Order.Ascending)
    """The order by which to list the groups."""
