"""
Copyright (c) Cutleast
"""

from enum import Enum

from pydantic_xml import BaseXmlModel, attr, element

from .dependency_type_group import DependencyTypesGroup


class CompositeDependency(BaseXmlModel, search_mode="unordered"):
    """
    Model representing the compositeDependency tag of the ModuleConfig.xml.

    A dependency that is made up of one or more dependencies.
    """

    dependencies: DependencyTypesGroup = element(tag="dependencies")
    """A list of dependencies."""

    class Operator(Enum):
        """Enum for the relation of the contained dependencies."""

        And = "And"
        """
        Indicates all contained dependencies must be satisfied in order for this
        dependency to be satisfied.
        """

        Or = "Or"
        """
        Indicates at least one listed dependency must be satisfied in order for this
        dependency to be satisfied.
        """

    operator: Operator = attr(name="operator", default=Operator.And)
    """The relation of the contained dependencies."""
