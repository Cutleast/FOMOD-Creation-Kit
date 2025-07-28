"""
Copyright (c) Cutleast
"""

from __future__ import annotations

import logging
import shutil
from pathlib import Path
from typing import Optional, override

from lxml import etree

from ui.widgets.loading_dialog import LoadingDialog

from .exceptions import NotAFomodError, XmlValidationError
from .fomod_info import FomodInfo
from .module_config.module_config import ModuleConfig
from .module_config.module_title import ModuleTitle


class Fomod:
    """
    Class representing a loaded FOMOD installer.
    """

    path: Optional[Path] = None
    """The path to the root folder of this FOMOD installer."""

    info: FomodInfo
    """The metadata of this FOMOD installer."""

    module_config: ModuleConfig
    """The module config of this FOMOD installer."""

    log: logging.Logger = logging.getLogger("Fomod")

    def __init__(
        self, path: Optional[Path], info: FomodInfo, module_config: ModuleConfig
    ) -> None:
        self.path = path
        self.info = info
        self.module_config = module_config

    @property
    def name(self) -> str:
        """
        The name of the FOMOD installer.
        """

        return self.info.name

    @name.setter
    def name(self, new_name: str) -> None:
        """
        Sets the name of the FOMOD installer.

        Args:
            new_name (str): The new name of the FOMOD installer.
        """

        self.info.name = new_name
        self.module_config.module_name.title = new_name

    def finalize(
        self,
        path: Optional[Path] = None,
        validate_xml: bool = True,
        encoding: str = "utf-8",
        ldialog: Optional[LoadingDialog] = None,
    ) -> None:
        """
        Saves and finalizes the FOMOD by fetching all files and folders referenced by
        absolute paths in the installer, moving them to the root folder of the installer
        and updating the paths to be relative. Practically makes the entire mod ready
        to be packed in a zip file and distributed.

        Args:
            path (Path, optional):
                The path to finalize the FOMOD installer to. Defaults to the current.
            validate_xml (bool, optional):
                Whether to validate the XML files before saving. Defaults to True.
            encoding (str, optional):
                The encoding to use for the XML files. Defaults to "utf-8".
            ldialog (Optional[LoadingDialog], optional):
                Optional loading dialog to display progress in. Defaults to None.
        """

        if path is not None:
            if self.path is not None:
                self.__create_copy(path)

            self.path = path

        if self.path is None:
            raise ValueError("FOMOD path is not set.")

        from .finalizer import Finalizer

        Finalizer().finalize(self, ldialog)

        self.save(validate_xml, encoding)
        self.log.info("FOMOD finalized.")

    def __create_copy(self, new_path: Path) -> None:
        """
        Creates a copy of the FOMOD at the specified path.

        Args:
            new_path (Path): Path to copy the FOMOD to.

        Raises:
            ValueError: If the FOMOD path is not set.
        """

        if self.path is None:
            raise ValueError("FOMOD path is not set.")

        new_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(self.path.parent, new_path.parent, dirs_exist_ok=True)

    def save(self, validate_xml: bool = True, encoding: str = "utf-8") -> None:
        """
        Saves the FOMOD installer to its path.

        Args:
            validate_xml (bool, optional):
                Whether to validate the XML files before saving. Defaults to True.
            encoding (str, optional):
                The encoding to use for the XML files. Defaults to "utf-8".
        """

        if self.path is None:
            raise ValueError("FOMOD path is not set.")

        self.log.info(f"Saving FOMOD installer to '{self.path}'...")
        self.path.mkdir(parents=True, exist_ok=True)

        info_path: Path = self.path / "info.xml"
        module_config_path: Path = self.path / "ModuleConfig.xml"

        self.log.info(f"Saving info.xml to '{info_path}'...")

        try:
            info_path.write_bytes(self.info.dump(validate_xml))
        except etree.DocumentInvalid as ex:
            raise XmlValidationError(info_path.name) from ex

        self.log.info(f"Saving ModuleConfig.xml to '{module_config_path}'...")

        try:
            module_config_path.write_bytes(
                self.module_config.dump(validate_xml, encoding)
            )
        except etree.DocumentInvalid as ex:
            raise XmlValidationError(module_config_path.name) from ex

        self.log.info(f"Saved FOMOD installer to '{self.path}'.")

    def save_as(
        self, path: Path, validate_xml: bool = True, encoding: str = "utf-8"
    ) -> None:
        """
        Saves the FOMOD installer to the specified path.
        This changes this FOMOD instance's path.

        Args:
            path (Path): The path to save the FOMOD installer to.
            validate_xml (bool, optional):
                Whether to validate the XML files before saving. Defaults to True.
            encoding (str, optional):
                The encoding to use for the XML files. Defaults to "utf-8".
        """

        self.path = path
        self.save(validate_xml, encoding)

    @staticmethod
    def load(path: Path) -> Fomod:
        """
        Loads a FOMOD installer from the given path.

        Args:
            path (Path):
                The path to the FOMOD installer, can be the info.xml, the
                ModuleConfig.xml or a folder containing both.

        Returns:
            Fomod: Loaded FOMOD installer.
        """

        Fomod.log.info(f"Loading FOMOD installer from '{path}'...")

        info_path: Optional[Path] = None
        module_config_path: Optional[Path] = None
        if path.is_dir():
            info_path = path / "info.xml"
            module_config_path = path / "ModuleConfig.xml"
        elif path.name.lower() == "info.xml":
            info_path = path
            module_config_path = path.parent / "ModuleConfig.xml"
        elif path.name.lower() == "moduleconfig.xml":
            info_path = path.parent / "info.xml"
            module_config_path = path

        if (info_path is None or not info_path.is_file()) or (
            module_config_path is None or not module_config_path.is_file()
        ):
            raise NotAFomodError(path)

        info: FomodInfo = FomodInfo.load(info_path.read_bytes())
        module_config: ModuleConfig = ModuleConfig.load(module_config_path.read_bytes())

        Fomod.log.info(f"Loaded FOMOD installer with name '{info.name}'.")

        return Fomod(info_path.parent, info, module_config)

    @staticmethod
    def create() -> Fomod:
        """
        Creates a new FOMOD installer with the bare minimum.

        Returns:
            Fomod: Created FOMOD installer.
        """

        return Fomod(
            path=None,
            info=FomodInfo(name=""),
            module_config=ModuleConfig(module_name=ModuleTitle(title="")),
        )

    @override
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Fomod):
            return False

        return self.info == value.info and self.module_config == value.module_config
