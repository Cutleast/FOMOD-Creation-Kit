"""
Copyright (c) Cutleast
"""

from pathlib import Path

import pytest

from core.fomod.module_config.file_system.file_system_item import FileSystemItem
from tests.base_test import BaseTest


class TestFileSystemItem(BaseTest):
    """
    Tests `core.fomod.module_config.file_system.file_system_item.FileSystemItem`.
    """

    SERIALIZATION_TEST_DATA: list[tuple[FileSystemItem, str]] = [
        (
            FileSystemItem(source=Path("."), destination=Path(".")),
            '<FileSystemItem source="" destination=""/>',
        ),
        (
            FileSystemItem(source=Path(".")),
            '<FileSystemItem source=""/>',
        ),
        (
            FileSystemItem(source=Path("")),
            '<FileSystemItem source=""/>',
        ),
        (
            FileSystemItem(source=Path()),
            '<FileSystemItem source=""/>',
        ),
        (
            FileSystemItem(source=Path("Test\\lol/lol2")),
            '<FileSystemItem source="Test\\lol\\lol2"/>',
        ),
    ]

    @pytest.mark.parametrize("item, expected_xml", SERIALIZATION_TEST_DATA)
    def test_serialization_of_paths(
        self, item: FileSystemItem, expected_xml: str
    ) -> None:
        """
        Tests that empty paths are correctly serialized as "" instead of ".".
        """

        # when
        xml: str | bytes = item.to_xml(exclude_unset=True)
        if isinstance(xml, bytes):
            xml = xml.decode("utf-8")

        # then
        assert xml == expected_xml
