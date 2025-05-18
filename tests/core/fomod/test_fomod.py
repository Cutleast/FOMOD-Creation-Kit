"""
Copyright (c) Cutleast
"""

from pathlib import Path

from core.fomod.fomod import Fomod
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

        assert fomod.info.name == ""
        assert fomod.info.author == ""
        assert fomod.info.version.version == ""
        assert fomod.info.version.machine_version is None
        assert fomod.info.description == ""
        assert fomod.info.website == ""

        fomod.info.dump()
        fomod.module_config.dump()
