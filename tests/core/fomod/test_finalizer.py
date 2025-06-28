"""
Copyright (c) Cutleast
"""

from pathlib import Path

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

from core.fomod.finalizer import Finalizer
from core.fomod.fomod import Fomod
from core.fomod.module_config.condition.conditional_file_install_list import (
    ConditionalFileInstallList,
)
from core.fomod.module_config.condition.conditional_install_pattern_list import (
    ConditionalInstallPatternList,
)
from core.fomod.module_config.dependency.composite_dependency import CompositeDependency
from core.fomod.module_config.file_system.file_item import FileItem
from core.fomod.module_config.file_system.file_list import FileList
from core.fomod.module_config.header_image import HeaderImage
from core.fomod.module_config.image import Image
from core.fomod.module_config.install_step.group import Group
from core.fomod.module_config.install_step.group_list import GroupList
from core.fomod.module_config.install_step.install_step import InstallStep
from core.fomod.module_config.install_step.plugin_list import PluginList
from core.fomod.module_config.install_step.step_list import StepList
from core.fomod.module_config.plugin.plugin import Plugin
from core.fomod.module_config.plugin.plugin_type import PluginType
from core.fomod.module_config.plugin.plugin_type_descriptor import PluginTypeDescriptor
from tests.base_test import BaseTest
from tests.core.fomod.test_fomod import ConditionalInstallPattern


class TestFinalizer(BaseTest):
    """
    Tests `core.fomod.finalizer.Finalizer`.
    """

    @pytest.fixture
    def fomod(self, data_folder: Path) -> Fomod:
        """
        Fixture that creates and provides a Fomod instance for tests.
        """

        fomod: Fomod = Fomod.create()
        fomod.module_config.module_image = HeaderImage(
            path=data_folder / "Dynamic Interface Patcher FOMOD" / "fomod" / "Image.jpg"
        )
        fomod.module_config.required_install_files = FileList(
            files=[FileItem(source=data_folder / "TestFiles" / "test1.txt")]
        )
        fomod.module_config.conditional_file_installs = ConditionalFileInstallList(
            patterns=ConditionalInstallPatternList(
                patterns=[
                    ConditionalInstallPattern(
                        dependencies=CompositeDependency(),
                        files=FileList(
                            files=[
                                FileItem(source=data_folder / "TestFiles" / "test2.txt")
                            ]
                        ),
                    )
                ]
            )
        )
        fomod.module_config.install_steps = StepList(
            install_steps=[
                InstallStep(
                    name="Step 1",
                    optional_file_groups=GroupList(
                        groups=[
                            Group(
                                name="Group 1",
                                type=Group.Type.SelectAtLeastOne,
                                plugins=PluginList(
                                    plugins=[
                                        Plugin(
                                            name="Plugin 1",
                                            image=Image(
                                                path=data_folder
                                                / "Dynamic Interface Patcher FOMOD"
                                                / "fomod"
                                                / "Image.jpg"
                                            ),
                                            files=FileList(
                                                files=[
                                                    FileItem(
                                                        source=data_folder
                                                        / "TestFiles"
                                                        / "test2.txt"
                                                    )
                                                ]
                                            ),
                                            type_descriptor=PluginTypeDescriptor(
                                                type=PluginType(
                                                    name=PluginType.Type.Optional
                                                )
                                            ),
                                        )
                                    ]
                                ),
                            )
                        ]
                    ),
                )
            ]
        )

        return fomod

    def test_finalize(
        self,
        data_folder: Path,
        test_fs: FakeFilesystem,
        fomod: Fomod,
        trashbin: list[Path],
    ) -> None:
        """
        Tests the finalization of a FOMOD installer.
        """

        # given
        fomod.path = Path("FinalizeTestOutput").absolute() / "fomod"

        # when
        Finalizer().finalize(fomod)

        # then
        assert trashbin == []

        assert fomod.path.is_dir()
        assert (fomod.path / "ModuleImage" / "Image.jpg").is_file()
        assert (
            fomod.module_config.module_image is not None
            and fomod.module_config.module_image.path
            == Path("fomod") / "ModuleImage" / "Image.jpg"
        )

        assert (fomod.path / "files" / "required_install_files" / "test1.txt").is_file()
        assert (
            fomod.module_config.required_install_files is not None
            and fomod.module_config.required_install_files.files[0].source
            == Path("fomod") / "files" / "required_install_files" / "test1.txt"
        )

        assert (
            fomod.path / "files" / "conditional_install_files.0" / "test2.txt"
        ).is_file()
        assert (
            fomod.module_config.conditional_file_installs is not None
            and fomod.module_config.conditional_file_installs.patterns.patterns[0]
            .files.files[0]
            .source
            == Path("fomod") / "files" / "conditional_install_files.0" / "test2.txt"
        )

        assert (
            fomod.path
            / "files"
            / "install_steps"
            / "Step 1"
            / "Group 1"
            / "Plugin 1"
            / "test2.txt"
        ).is_file()
        assert (
            fomod.module_config.install_steps is not None
            and fomod.module_config.install_steps.install_steps[0]
            .optional_file_groups.groups[0]
            .plugins.plugins[0]
            .files
            is not None
            and fomod.module_config.install_steps.install_steps[0]
            .optional_file_groups.groups[0]
            .plugins.plugins[0]
            .files.files[0]
            .source
            == Path("fomod")
            / "files"
            / "install_steps"
            / "Step 1"
            / "Group 1"
            / "Plugin 1"
            / "test2.txt"
        )

        assert (
            fomod.path / "images" / "Step 1" / "Group 1" / "Plugin 1" / "Image.jpg"
        ).is_file()
        assert (
            fomod.module_config.install_steps.install_steps[0]
            .optional_file_groups.groups[0]
            .plugins.plugins[0]
            .image
            is not None
            and fomod.module_config.install_steps.install_steps[0]
            .optional_file_groups.groups[0]
            .plugins.plugins[0]
            .image.path
            == Path("fomod")
            / "images"
            / "Step 1"
            / "Group 1"
            / "Plugin 1"
            / "Image.jpg"
        )
