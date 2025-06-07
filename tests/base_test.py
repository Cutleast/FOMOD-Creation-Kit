"""
Copyright (c) Cutleast
"""

import time
from pathlib import Path

import pytest
from pyfakefs.fake_filesystem import FakeFilesystem

import resources_rc  # type: ignore # noqa: F401
from core.config.app_config import AppConfig
from core.config.behavior_config import BehaviorConfig
from core.utilities.logger import Logger


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

        return Path("tests").absolute() / "data"

    @pytest.fixture
    def real_cwd(self) -> Path:
        """
        Returns:
            Path: The real current working directory (outside of the fake filesystem).
        """

        return Path.cwd()

    @pytest.fixture
    def app_config(self, data_folder: Path) -> AppConfig:
        """
        Returns the application config for the tests.

        Returns:
            AppConfig: The application config.
        """

        return AppConfig.load(data_folder / "config")

    @pytest.fixture
    def behavior_config(self, data_folder: Path) -> BehaviorConfig:
        """
        Returns the behavior config for the tests.

        Returns:
            BehaviorConfig: The behavior config.
        """

        return BehaviorConfig.load(data_folder / "config")

    @pytest.fixture
    def test_fs(
        self, real_cwd: Path, data_folder: Path, fs: FakeFilesystem
    ) -> FakeFilesystem:
        """
        Creates a fake filesystem for testing.

        Returns:
            FakeFilesystem: The fake filesystem.
        """

        fs.add_real_directory(data_folder)

        # Add qtawesome fonts
        fs.add_real_directory(
            real_cwd / ".venv" / "lib" / "site-packages" / "qtawesome" / "fonts"
        )

        return fs

    @pytest.fixture
    def logger(self, test_fs: FakeFilesystem, app_config: AppConfig) -> Logger:
        """
        Creates a logger instance for tests.

        Returns:
            Logger: The logger instance.
        """

        log_path: Path = Path("test_logs")
        log_path.mkdir(parents=True, exist_ok=True)
        log_file: Path = log_path / time.strftime(app_config.log_file_name)

        return Logger(log_file, app_config.log_format, app_config.log_date_format)

    @pytest.fixture
    def trashbin(self, monkeypatch: pytest.MonkeyPatch) -> list[Path]:
        """
        Fixture to mock the trashbin using a list of paths.
        Patches `send2trash.send2trash` to append the path to the list.
        """

        trashbin: list[Path] = []

        monkeypatch.setattr("send2trash.send2trash", trashbin.append)

        return trashbin
