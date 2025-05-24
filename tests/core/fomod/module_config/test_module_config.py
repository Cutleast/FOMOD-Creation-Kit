"""
Copyright (c) Cutleast
"""

from pathlib import Path

from pyfakefs.fake_filesystem import FakeFilesystem

from core.fomod.fomod import Fomod
from core.fomod.module_config.dependency.composite_dependency import CompositeDependency
from core.fomod.module_config.dependency.file_dependency import FileDependency
from core.fomod.module_config.file_system_item import FileSystemItem
from core.fomod.module_config.group import Group
from core.fomod.module_config.install_step import InstallStep
from core.fomod.module_config.module_config import ModuleConfig
from core.fomod.module_config.order import Order
from core.fomod.module_config.plugin import Plugin
from core.fomod.module_config.plugin_type import PluginType
from core.fomod.module_config.plugin_type_descriptor import PluginTypeDescriptor
from tests.base_test import BaseTest


class TestModuleConfig(BaseTest):
    """
    Tests `core.fomod.module_config.ModuleConfig`.
    """

    def test_load(self, data_folder: Path, test_fs: FakeFilesystem) -> None:
        """
        Tests the loading of a ModuleConfig.xml file.
        """

        # given
        module_config_file: Path = data_folder / "TestModuleConfig" / "ModuleConfig.xml"

        # when
        module_config: ModuleConfig = ModuleConfig.load(module_config_file.read_bytes())

        # then
        assert module_config.module_name.title == "Dynamic Interface Patcher - DIP"
        assert module_config.install_steps is not None
        assert len(module_config.install_steps.install_steps) == 1

        # when
        install_step: InstallStep = module_config.install_steps.install_steps[0]

        # then
        assert install_step.name == "Installation Process"
        assert install_step.optional_file_groups.order == Order.Explicit
        assert len(install_step.optional_file_groups.groups) == 1

        # when
        group: Group = install_step.optional_file_groups.groups[0]

        # then
        assert group.name == "Do you know what you're doing?"
        assert group.type == Group.Type.SelectAtLeastOne
        assert group.plugins.order == Order.Explicit
        assert len(group.plugins.plugins) == 1

        # when
        plugin: Plugin = group.plugins.plugins[0]

        # then
        assert plugin.name == "Proceed"
        assert plugin.description.startswith("Before you install this tool,")
        assert plugin.image is not None
        assert str(plugin.image.path) == "fomod\\Image.jpg"
        assert plugin.files is not None
        assert len(plugin.files.files) == 0
        assert len(plugin.files.folders) == 1
        assert plugin.type_descriptor is not None

        # when
        folder: FileSystemItem = plugin.files.folders[0]

        # then
        assert str(folder.source) == "fomod\\DIP"
        assert str(folder.destination) == "DIP"
        assert folder.priority == 0

        # when
        type_descriptor: PluginTypeDescriptor = plugin.type_descriptor

        # then
        assert type_descriptor.dependency_type is None
        assert type_descriptor.type is not None
        assert type_descriptor.type.name == PluginType.Type.Optional

    def test_dump(self, data_folder: Path, test_fs: FakeFilesystem) -> None:
        """
        Tests the saving of a FOMOD module config file.
        """

        # given
        module_config_file: Path = data_folder / "TestModuleConfig" / "ModuleConfig.xml"
        output_info_file: Path = Path("ModuleConfig.xml")
        module_config: ModuleConfig = ModuleConfig.load(module_config_file.read_bytes())

        # when
        module_config.module_name.title = "New Name"
        output_info_file.write_bytes(module_config.dump())
        edited_module_config: ModuleConfig = ModuleConfig.load(
            output_info_file.read_bytes()
        )

        # then
        assert edited_module_config.module_name.title == "New Name"
        assert (
            edited_module_config.module_dependencies
            == module_config.module_dependencies
        )
        assert (
            edited_module_config.required_install_files
            == module_config.required_install_files
        )
        assert edited_module_config.install_steps == module_config.install_steps
        assert (
            edited_module_config.conditional_file_installs
            == module_config.conditional_file_installs
        )

    def test_add_module_dependency(self, test_fs: FakeFilesystem) -> None:
        """
        Tests adding a module dependency to the module config and that it's saved
        correctly.
        """

        # given
        fomod: Fomod = Fomod.create()
        dependency = CompositeDependency(
            file_dependencies=[
                FileDependency(file="test.esp", state=FileDependency.State.Inactive)
            ],
        )
        fomod_path = Path("fomod")

        # when
        fomod.module_config.module_dependencies = dependency
        fomod.save_as(fomod_path, encoding="utf-16le")

        reloaded_fomod: Fomod = Fomod.load(fomod_path)

        # then
        assert reloaded_fomod.module_config.module_dependencies == dependency
