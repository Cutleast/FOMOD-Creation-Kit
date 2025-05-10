"""
Copyright (c) Cutleast
"""

from pathlib import Path

from pyfakefs.fake_filesystem import FakeFilesystem

from core.fomod.module_config.module_config import ModuleConfig
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
        assert len(module_config.install_steps.install_steps) == 1

    def test_dump(self, data_folder: Path, test_fs: FakeFilesystem) -> None:
        """
        Tests the saving of a FOMOD info file.
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
