"""
Copyright (c) Cutleast
"""

from pathlib import Path

from pyfakefs.fake_filesystem import FakeFilesystem

from core.fomod.fomod_info import FomodInfo
from tests.base_test import BaseTest


class TestFomodInfo(BaseTest):
    """
    Tests `core.fomod.fomod_info.FomodInfo`.
    """

    def test_load(self, data_folder: Path, test_fs: FakeFilesystem) -> None:
        """
        Tests the loading of a FOMOD info file.
        """

        # given
        fomod_info_file: Path = data_folder / "TestFomodInfo" / "info.xml"

        # when
        fomod_info: FomodInfo = FomodInfo.load(fomod_info_file.read_bytes())

        # then
        assert fomod_info.name == "Dynamic Interface Patcher - DIP"
        assert fomod_info.author == "Cutleast"
        assert fomod_info.version.value == "2.1.5"
        assert fomod_info.version.machine_version is None
        assert (
            fomod_info.website
            == "https://www.nexusmods.com/skyrimspecialedition/mods/96891"
        )
        assert fomod_info.description == (
            "A dynamic patching tool for ui mods with strict permissions like "
            "RaceMenu or MiniMap."
        )

    def test_dump(self, data_folder: Path, test_fs: FakeFilesystem) -> None:
        """
        Tests the saving of a FOMOD info file.
        """

        # given
        fomod_info_file: Path = data_folder / "TestFomodInfo" / "info.xml"
        output_info_file: Path = Path("info.xml")
        fomod_info: FomodInfo = FomodInfo.from_xml(fomod_info_file.read_bytes())

        # when
        fomod_info.name = "New Name"
        output_info_file.write_bytes(fomod_info.dump())
        edited_fomod_info: FomodInfo = FomodInfo.from_xml(output_info_file.read_bytes())

        # then
        assert edited_fomod_info.name == "New Name"
