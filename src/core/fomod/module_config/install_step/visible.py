"""
Copyright (c) Cutleast
"""

from pydantic_xml import BaseXmlModel, element

from ..dependency.composite_dependency import CompositeDependency


class Visible(BaseXmlModel):
    """
    Model representing conditions for an install step to be visible.
    """

    dependencies: CompositeDependency = element(tag="dependencies")
    """The dependencies that must be met for the install step to be visible."""
