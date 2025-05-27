"""
Copyright (c) Cutleast
"""

from core.fomod.module_config.plugin.plugin_type_descriptor import PluginTypeDescriptor
from tests.base_test import BaseTest


class TestPluginTypeDescriptor(BaseTest):
    """
    Tests `core.fomod.module_config.plugin_type_descriptor.PluginTypeDescriptor`.
    """

    def test_from_xml(self) -> None:
        """
        Tests the deserialization of a PluginTypeDescriptor element.
        """

        # given
        xml_text: str = """
<PluginTypeDescriptor> 
    <dependencyType> 
        <defaultType name="Optional"/> 
        <patterns> 
            <pattern> 
                <dependencies operator="And"> 
                    <fileDependency file="Skyrim Unification Project_Resources.esp" state="Active"/> 
                </dependencies> 
                <type name="Recommended"/> 
            </pattern> 
        </patterns> 
    </dependencyType> 
</PluginTypeDescriptor> 
"""

        # when
        plugin_type_descriptor: PluginTypeDescriptor = PluginTypeDescriptor.from_xml(
            xml_text
        )

        # then
        assert plugin_type_descriptor.dependency_type is not None
        assert plugin_type_descriptor.type is None
