"""
Copyright (c) Cutleast
"""

from core.fomod.module_config.condition.condition_flag_list import ConditionFlagList
from core.fomod.module_config.dependency.composite_dependency import CompositeDependency
from core.fomod.module_config.dependency.dependency_pattern_list import (
    DependencyPatternList,
)
from core.fomod.module_config.dependency.dependency_plugin_type import (
    DependencyPluginType,
)
from core.fomod.module_config.dependency.file_dependency import FileDependency
from core.fomod.module_config.plugin.plugin import Plugin
from core.fomod.module_config.plugin.plugin_type import PluginType
from core.fomod.module_config.plugin.plugin_type_descriptor import PluginTypeDescriptor
from tests.base_test import BaseTest


class TestPlugin(BaseTest):
    """
    Tests `core.fomod.module_config.plugin.Plugin`.
    """

    def test_from_xml(self) -> None:
        """
        Tests the deserialization of a Plugin element.
        """

        # given
        xml_text: str = """
<Plugin name="JK's Angeline's Aromatics">
    <description></description>
    <conditionFlags>
        <flag name="Angeline">On</flag>
    </conditionFlags>
    <typeDescriptor>
        <dependencyType>
            <defaultType name="Optional"/>
            <patterns>
                <pattern>
                    <dependencies operator="Or">
                        <fileDependency file="JK's Angelines Aromatics.esp" state="Active"/>
                    </dependencies>
                    <type name="Recommended"/>
                </pattern>
            </patterns>
        </dependencyType>
    </typeDescriptor>
</Plugin>
"""

        # when
        plugin: Plugin = Plugin.from_xml(xml_text)

        # then
        assert plugin.name == "JK's Angeline's Aromatics"
        assert plugin.description == "JK's Angeline's Aromatics"
        assert plugin.condition_flags is not None
        assert plugin.files is None

        # when
        condition_flags: ConditionFlagList = plugin.condition_flags

        # then
        assert len(condition_flags.flags) == 1
        assert condition_flags.flags[0].name == "Angeline"
        assert condition_flags.flags[0].value == "On"

        # when
        type_descriptor: PluginTypeDescriptor = plugin.type_descriptor

        # then
        assert type_descriptor.dependency_type is not None
        assert type_descriptor.type is None

        # when
        dependency_type: DependencyPluginType = type_descriptor.dependency_type

        # then
        assert dependency_type.default_type.name == PluginType.Type.Optional

        # when
        patterns: DependencyPatternList = dependency_type.patterns

        # then
        assert len(patterns.patterns) == 1
        assert patterns.patterns[0].type.name == PluginType.Type.Recommended

        # when
        composite_dependency: CompositeDependency = patterns.patterns[0].dependencies

        # then
        assert composite_dependency.operator == CompositeDependency.Operator.Or
        assert len(composite_dependency.file_dependencies) == 1
        assert len(composite_dependency.flag_dependencies) == 0
        assert composite_dependency.game_dependency is None
        assert composite_dependency.fomm_dependency is None
        assert composite_dependency.dependencies == []

        # when
        file_dependency: FileDependency = composite_dependency.file_dependencies[0]

        # then
        assert file_dependency.file == "JK's Angelines Aromatics.esp"
        assert file_dependency.state == FileDependency.State.Active
