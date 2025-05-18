"""
Copyright (c) Cutleast
"""

from core.fomod.module_config.dependency.composite_dependency import CompositeDependency
from tests.base_test import BaseTest


class TestCompositeDependency(BaseTest):
    """
    Tests `core.fomod.module_config.dependency.composite_dependency.CompositeDependency`.
    """

    def test_from_xml(self) -> None:
        """
        Tests the deserialization of a CompositeDependency element.
        """

        # given
        xml_text: str = """
<dependencies>
    <dependencies>
        <fileDependency file="test.txt" state="Missing" />
    </dependencies>
</dependencies>
"""

        # when
        composite_dependency: CompositeDependency = CompositeDependency.from_xml(
            xml_text
        )

        # then
        assert composite_dependency.dependencies.dependencies is None
        assert composite_dependency.dependencies.file_dependencies[0].file == "test.txt"
