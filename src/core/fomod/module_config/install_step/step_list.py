"""
Copyright (c) Cutleast
"""

from pydantic_xml import BaseXmlModel, attr, element

from .install_step import InstallStep
from .order import Order


class StepList(BaseXmlModel):
    """
    Model representing a list of install steps.
    """

    install_steps: list[InstallStep] = element(tag="installStep")
    """A list of install steps for the mod."""

    order: Order = attr(name="order", default=Order.Ascending)
    """The order by which to list the steps."""
