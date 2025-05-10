"""
Copyright (c) Cutleast
"""

from pydantic_xml import BaseXmlModel, attr, element

from .order import Order
from .plugin import Plugin


class PluginList(BaseXmlModel):
    """
    Model representing a list of plugins.
    """

    plugins: list[Plugin] = element(tag="plugin")
    """A list of plugins belonging to a group."""

    order: Order = attr(name="order", default=Order.Ascending)
    """The order by which to list the plugins."""
