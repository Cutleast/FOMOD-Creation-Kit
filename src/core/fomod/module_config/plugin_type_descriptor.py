"""
Copyright (c) Cutleast
"""

from typing import Optional, Self

from pydantic import model_validator
from pydantic_xml import BaseXmlModel, element

from .dependency.dependency_plugin_type import DependencyPluginType
from .plugin_type import PluginType


class PluginTypeDescriptor(BaseXmlModel):
    """
    Model representing a plugin type descriptor.
    """

    dependency_type: Optional[DependencyPluginType] = element(
        name="dependencyType", default=None
    )
    """
    Used when the plugin type is dependent upon the state of other mods.
    Mutual exclusive with `type`.
    """

    type: Optional[PluginType] = element(name="type", default=None)
    """The type of the plugin. Mutual exclusive with `dependency_type`."""

    @model_validator(mode="after")
    def check_exclusivity(self) -> Self:
        # TODO: Reevaluate this
        if self.dependency_type is not None and self.type is not None:
            raise ValueError("dependency_type and type are mutually exclusive!")
        elif self.dependency_type is None and self.type is None:
            raise ValueError(
                "dependency_type and type are both missing but one is required!"
            )

        return self
