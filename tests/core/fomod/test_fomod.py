"""
Copyright (c) Cutleast
"""

from pathlib import Path

from core.fomod.fomod import Fomod
from core.fomod.module_config.dependency.composite_dependency import CompositeDependency
from core.fomod.module_config.group import Group
from core.fomod.module_config.install_step import InstallStep
from core.fomod.module_config.plugin import Plugin
from tests.base_test import BaseTest


class TestFomod(BaseTest):
    """
    Tests `core.fomod.fomod.Fomod`.
    """

    def test_load(self, data_folder: Path) -> None:
        """
        Test `Fomod.load()`.
        """

        # given
        fomod_path: Path = (
            data_folder / "JK's Interiors Patch Collection FOMOD" / "fomod"
        )

        # when
        fomod: Fomod = Fomod.load(fomod_path)

        # then
        assert fomod.info.name == "JK's Interiors Patch Collection"
        assert fomod.module_config.install_steps is not None

        # when
        install_step: InstallStep = fomod.module_config.install_steps.install_steps[1]

        # then
        assert install_step.name == "Additional files verification"
        assert install_step.visible[0].operator == CompositeDependency.Operator.And

        # when
        group: Group = install_step.optional_file_groups.groups[0]

        # then
        assert group.name == "Would you like to remove duplicate unique items?"
        assert len(group.plugins.plugins) == 2

        # when
        yes_plugin: Plugin = group.plugins.plugins[0]

        # then
        assert yes_plugin.name == "Yes 💬"
        assert yes_plugin.description.startswith("💬 - ")
        assert yes_plugin.condition_flags is not None
        assert len(yes_plugin.condition_flags.flags) == 1
        assert yes_plugin.condition_flags.flags[0].name == "Immersion"
        assert yes_plugin.condition_flags.flags[0].value == "On"
        assert yes_plugin.type_descriptor.dependency_type is not None

    def test_create(self) -> None:
        """
        Tests `Fomod.create()`.
        """

        # when
        fomod: Fomod = Fomod.create()

        # then
        assert fomod.info is not None
        assert fomod.module_config is not None
        assert fomod.path is None

        assert fomod.info.name == "default"
        assert fomod.info.author == ""
        assert fomod.info.version.version == ""
        assert fomod.info.version.machine_version is None
        assert fomod.info.description == ""
        assert fomod.info.website == ""

        assert fomod.module_config.module_name.title == "default"

        fomod.info.dump()
        fomod.module_config.dump()
