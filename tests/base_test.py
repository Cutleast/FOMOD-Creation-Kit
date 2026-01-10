"""
Copyright (c) Cutleast
"""

import time
from pathlib import Path

import pytest
from cutleast_core_lib.core.utilities.logger import Logger
from cutleast_core_lib.test.base_test import BaseTest as CoreBaseTest
from pyfakefs.fake_filesystem import FakeFilesystem

import resources_rc as resources_rc
from core.config.app_config import AppConfig
from core.config.behavior_config import BehaviorConfig
from core.fomod_editor.history import History


class BaseTest(CoreBaseTest):
    """
    Base class for all tests.
    """

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

    @pytest.fixture
    def history(self, test_fs: FakeFilesystem) -> History:
        """
        Returns a history instance for tests.

        Returns:
            History: The history instance.
        """

        return History(Path("data"))
