"""
Copyright (c) Cutleast
"""

from pathlib import Path

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

import resources_rc  # type: ignore # noqa: F401
from core.config.app_config import AppConfig


class BaseTest:
    """
    Base class for all tests.
    """

    @pytest.fixture
    def data_folder(self) -> Path:
        """
        Returns the path to the test data folder.

        Returns:
            Path: The path to the test data folder.
        """

        return Path("tests") / "data"

    @pytest.fixture
    def app_config(self, data_folder: Path) -> AppConfig:
        """
        Returns the application config for the tests.

        Returns:
            AppConfig: The application config.
        """

        return AppConfig.load(data_folder / "config")

    @pytest.fixture
    def test_fs(self, data_folder: Path, fs: FakeFilesystem) -> FakeFilesystem:
        """
        Creates a fake filesystem for testing.

        Returns:
            FakeFilesystem: The fake filesystem.
        """

        fs.add_real_directory(data_folder)

        return fs
