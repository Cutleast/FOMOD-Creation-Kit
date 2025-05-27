"""
Copyright (c) Cutleast
"""

from core.fomod.module_config.dependency.composite_dependency import CompositeDependency
from core.fomod.module_config.dependency.dependency_pattern import DependencyPattern
from core.fomod.module_config.dependency.file_dependency import FileDependency
from core.fomod.module_config.plugin.plugin_type import PluginType
from tests.base_test import BaseTest


class TestDependencyPattern(BaseTest):
    """
    Tests `core.fomod.module_config.dependency.dependency_pattern.DependencyPattern`.
    """

    def test_from_xml(self) -> None:
        """
        Tests the deserialization of a DependencyPattern element.
        """

        # given
        xml_text: str = """
<DependencyPattern> 
    <dependencies operator="Or"> 
        <fileDependency file="JK's Angelines Aromatics.esp" state="Active"/> 
    </dependencies> 
    <type name="Recommended"/> 
</DependencyPattern> 
"""

        # when
        dependency_pattern: DependencyPattern = DependencyPattern.from_xml(xml_text)

        # then
        assert (
            dependency_pattern.dependencies.operator == CompositeDependency.Operator.Or
        )
        assert dependency_pattern.type.name == PluginType.Type.Recommended

        # when
        dependency: CompositeDependency = dependency_pattern.dependencies

        # then
        assert len(dependency.file_dependencies) == 1
        assert len(dependency.flag_dependencies) == 0
        assert dependency.game_dependency is None
        assert dependency.fomm_dependency is None
        assert dependency.dependencies == []

        assert dependency.file_dependencies[0].file == "JK's Angelines Aromatics.esp"
        assert dependency.file_dependencies[0].state == FileDependency.State.Active
