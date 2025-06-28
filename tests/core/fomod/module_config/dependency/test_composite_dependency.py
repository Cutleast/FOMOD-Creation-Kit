"""
Copyright (c) Cutleast
"""

import pytest

from core.fomod.module_config.dependency.composite_dependency import CompositeDependency
from core.fomod.module_config.dependency.file_dependency import FileDependency
from core.fomod.module_config.dependency.flag_dependency import FlagDependency
from core.fomod.module_config.dependency.version_dependency import VersionDependency
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
<CompositeDependency operator="Or">
    <fileDependency file="test.txt" state="Missing" />
</CompositeDependency>
"""

        # when
        composite_dependency: CompositeDependency = CompositeDependency.from_xml(
            xml_text
        )

        # then
        assert composite_dependency.operator == CompositeDependency.Operator.Or
        assert composite_dependency.file_dependencies[0].file == "test.txt"
        assert composite_dependency.dependencies == []

    DISPLAY_NAME_DATA: list[tuple[CompositeDependency, str]] = [
        (
            CompositeDependency(
                file_dependencies=[
                    FileDependency(file="test.txt", state=FileDependency.State.Missing),
                    FileDependency(file="test2.txt", state=FileDependency.State.Active),
                ],
                flag_dependencies=[FlagDependency(flag="test", value="true")],
                game_dependency=VersionDependency(version="1.0.0"),
                dependencies=[
                    CompositeDependency(
                        game_dependency=VersionDependency(version="2.0.0")
                    )
                ],
                operator=CompositeDependency.Operator.Or,
            ),
            "test.txt (Missing), test2.txt (Active), test=true, Game Version=1.0.0 or Game Version=2.0.0",
        ),
        (
            CompositeDependency(
                game_dependency=VersionDependency(version="1.0.0"),
                dependencies=[
                    CompositeDependency(
                        file_dependencies=[
                            FileDependency(
                                file="test.txt", state=FileDependency.State.Missing
                            ),
                            FileDependency(
                                file="test2.txt", state=FileDependency.State.Active
                            ),
                        ],
                        game_dependency=VersionDependency(version="2.0.0"),
                    )
                ],
                operator=CompositeDependency.Operator.Or,
            ),
            "Game Version=1.0.0 or (test.txt (Missing), test2.txt (Active) and Game Version=2.0.0)",
        ),
        (
            CompositeDependency(
                game_dependency=VersionDependency(version="1.0.0"),
                operator=CompositeDependency.Operator.Or,
            ),
            "Game Version=1.0.0",
        ),
    ]

    @pytest.mark.parametrize("dependency, expected_display_name", DISPLAY_NAME_DATA)
    def test_get_display_name(
        self, dependency: CompositeDependency, expected_display_name: str
    ) -> None:
        """
        Tests the generation of a display name for a CompositeDependency.
        """

        # when
        display_name: str = dependency.get_display_name()

        # then
        assert display_name == expected_display_name
