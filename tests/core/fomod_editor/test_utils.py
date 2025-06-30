"""
Copyright (c) Cutleast
"""

import pytest

from core.fomod.fomod import Fomod
from core.fomod.module_config.condition.condition_flag_list import ConditionFlagList
from core.fomod.module_config.condition.conditional_file_install_list import (
    ConditionalFileInstallList,
)
from core.fomod.module_config.condition.conditional_install_pattern import (
    ConditionalInstallPattern,
)
from core.fomod.module_config.condition.conditional_install_pattern_list import (
    ConditionalInstallPatternList,
)
from core.fomod.module_config.condition.set_condition_flag import SetConditionFlag
from core.fomod.module_config.dependency.composite_dependency import CompositeDependency
from core.fomod.module_config.dependency.default_plugin_type import DefaultPluginType
from core.fomod.module_config.dependency.dependency_pattern import DependencyPattern
from core.fomod.module_config.dependency.dependency_plugin_type import (
    DependencyPatternList,
    DependencyPluginType,
)
from core.fomod.module_config.dependency.flag_dependency import FlagDependency
from core.fomod.module_config.file_system.file_list import FileList
from core.fomod.module_config.install_step.install_step import InstallStep
from core.fomod.module_config.install_step.step_list import StepList
from core.fomod.module_config.install_step.visible import Visible
from core.fomod.module_config.plugin.plugin import Plugin
from core.fomod.module_config.plugin.plugin_type import PluginType
from core.fomod.module_config.plugin.plugin_type_descriptor import PluginTypeDescriptor
from core.fomod_editor.utils import Utils
from tests.base_test import BaseTest


class TestUtils(BaseTest):
    """
    Tests `core.fomod_editor.utils.Utils`.
    """

    def test_get_fomod_flag_names(self) -> None:
        """
        Tests the collection of flag names from a Fomod.
        """

        # given
        fomod: Fomod = Fomod.create()
        fomod.module_config.conditional_file_installs = ConditionalFileInstallList(
            patterns=ConditionalInstallPatternList(
                patterns=[
                    ConditionalInstallPattern(
                        dependencies=CompositeDependency(
                            flag_dependencies=[
                                FlagDependency(flag="test", value="true"),
                                FlagDependency(flag="test2", value="false"),
                            ]
                        ),
                        files=FileList(),
                    )
                ]
            )
        )
        install_step: InstallStep = InstallStep.create()
        install_step.visible = Visible(
            dependencies=CompositeDependency(
                flag_dependencies=[
                    FlagDependency(flag="test2", value="true"),
                    FlagDependency(flag="test3", value="true"),
                ]
            )
        )
        fomod.module_config.install_steps = StepList(install_steps=[install_step])

        # when
        flag_names: list[str] = Utils.get_fomod_flag_names(fomod)

        # then
        assert flag_names == ["test", "test2", "test3"]

    FLAGS_FROM_COMP_DEP_DATA: list[tuple[CompositeDependency, list[str]]] = [
        (
            CompositeDependency(
                flag_dependencies=[
                    FlagDependency(flag="test", value="true"),
                    FlagDependency(flag="test2", value="false"),
                ],
                dependencies=[
                    CompositeDependency(
                        flag_dependencies=[
                            FlagDependency(flag="test3", value="true"),
                            FlagDependency(flag="test4", value="false"),
                        ]
                    )
                ],
            ),
            ["test", "test2", "test3", "test4"],
        ),
        (CompositeDependency(), []),
    ]

    @pytest.mark.parametrize(
        "dependency, expected_flag_names", FLAGS_FROM_COMP_DEP_DATA
    )
    def test_get_flag_names_from_composite_dependency(
        self, dependency: CompositeDependency, expected_flag_names: list[str]
    ) -> None:
        """
        Tests the collection of flag names from a CompositeDependency.
        """

        # when
        flag_names: list[str] = Utils.get_flag_names_from_composite_dependency(
            dependency
        )

        # then
        assert flag_names == expected_flag_names

    FLAGS_FROM_PLUGIN_DATA: list[tuple[Plugin, list[str]]] = [
        (
            Plugin(
                name="Test",
                condition_flags=ConditionFlagList(
                    flags=[
                        SetConditionFlag(name="test", value="true"),
                        SetConditionFlag(name="test2", value="false"),
                    ]
                ),
                type_descriptor=PluginTypeDescriptor(
                    dependency_type=DependencyPluginType(
                        default_type=DefaultPluginType(name=PluginType.Type.Optional),
                        patterns=DependencyPatternList(
                            patterns=[
                                DependencyPattern(
                                    dependencies=CompositeDependency(
                                        flag_dependencies=[
                                            FlagDependency(flag="test3", value="true"),
                                            FlagDependency(flag="test4", value="false"),
                                        ]
                                    ),
                                    type=PluginType(name=PluginType.Type.Recommended),
                                )
                            ]
                        ),
                    )
                ),
            ),
            ["test", "test2", "test3", "test4"],
        ),
        (Plugin.create(), []),
    ]

    @pytest.mark.parametrize("plugin, expected_flag_names", FLAGS_FROM_PLUGIN_DATA)
    def test_get_flag_names_from_plugin(
        self, plugin: Plugin, expected_flag_names: list[str]
    ) -> None:
        """
        Tests the collection of flag names from a Plugin.
        """

        # when
        flag_names: list[str] = Utils.get_flag_names_from_plugin(plugin)

        # then
        assert flag_names == expected_flag_names
