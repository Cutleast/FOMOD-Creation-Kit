"""
Copyright (c) Cutleast
"""

from pathlib import Path

from pyfakefs.fake_filesystem import FakeFilesystem

from core.fomod.fomod import Fomod
from core.fomod.module_config.dependency.composite_dependency import CompositeDependency
from core.fomod.module_config.group import Group
from core.fomod.module_config.header_image import HeaderImage
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

    def test_finalize(self, data_folder: Path, test_fs: FakeFilesystem) -> None:
        """
        Tests the finalization of a FOMOD installer and the correct inclusion of files
        from outside of it.
        """

        # given
        fomod: Fomod = Fomod.create()
        fomod_path = Path("test_output") / "fomod"
        fomod.module_config.module_image = HeaderImage(
            path=data_folder.absolute()
            / "Dynamic Interface Patcher FOMOD"
            / "fomod"
            / "Image.jpg"
        )

        # when
        fomod.finalize(fomod_path)

        # then
        assert fomod.path is not None
        assert fomod.path == fomod_path
        assert fomod.path.is_dir()

        # when
        images_path: Path = fomod.path / "images"

        # then
        assert images_path.is_dir()

        # when
        image_path: Path = images_path / "module.jpg"

        # then
        assert image_path.is_file()
        assert fomod.module_config.module_image.path == image_path.relative_to(
            fomod.path.parent
        )
