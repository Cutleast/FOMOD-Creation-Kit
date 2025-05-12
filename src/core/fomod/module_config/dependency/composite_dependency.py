"""
Copyright (c) Cutleast
"""

from typing import override

from pydantic_xml import BaseXmlModel, attr, element
from PySide6.QtWidgets import QApplication

from core.utilities.localized_enum import LocalizedEnum

from .dependency_type_group import DependencyTypesGroup


class CompositeDependency(BaseXmlModel, search_mode="unordered"):
    """
    Model representing the compositeDependency tag of the ModuleConfig.xml.

    A dependency that is made up of one or more dependencies.
    """

    dependencies: DependencyTypesGroup = element(tag="dependencies")
    """A list of dependencies."""

    class Operator(LocalizedEnum):
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

        @override
        def get_localized_name(self) -> str:
            locs: dict[CompositeDependency.Operator, str] = {
                CompositeDependency.Operator.And: QApplication.translate(
                    "CompositeDependency", "And"
                ),
                CompositeDependency.Operator.Or: QApplication.translate(
                    "CompositeDependency", "Or"
                ),
            }

            return locs[self]

        @override
        def get_localized_description(self) -> str:
            locs: dict[CompositeDependency.Operator, str] = {
                CompositeDependency.Operator.And: QApplication.translate(
                    "CompositeDependency",
                    "All contained dependencies must be satisfied in order for this "
                    "dependency to be satisfied.",
                ),
                CompositeDependency.Operator.Or: QApplication.translate(
                    "CompositeDependency",
                    "At least one listed dependency must be satisfied in order for this "
                    "dependency to be satisfied.",
                ),
            }

            return locs[self]

    operator: Operator = attr(name="operator", default=Operator.And)
    """The relation of the contained dependencies."""
