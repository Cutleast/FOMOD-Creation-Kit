"""
Copyright (c) Cutleast
"""

from __future__ import annotations

import logging
import shutil
from pathlib import Path
from typing import Optional

from lxml import etree

from core.fomod.module_config.plugin.plugin import Plugin

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

    def finalize(
        self,
        path: Optional[Path] = None,
        validate_xml: bool = True,
        encoding: str = "utf-8",
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
        """

        if path is not None:
            self.path = path

        if self.path is None:
            raise ValueError("FOMOD path is not set.")

        self.log.info(f"Finalizing FOMOD installer to '{self.path}'...")
        self.path.mkdir(parents=True, exist_ok=True)

        self.__include_images()
        self.__include_required_files()
        self.__include_conditional_files()

        self.save(validate_xml, encoding)
        self.log.info("FOMOD finalized.")

    def __include_images(self) -> None:
        if self.path is None:
            raise ValueError("FOMOD path is not set.")

        self.log.info("Including images...")

        images_path = self.path / "images"

        # TODO: Implement better way to clean up
        # if images_path.is_dir():
        #     shutil.rmtree(images_path)

        images_path.mkdir(parents=True, exist_ok=True)

        if (
            self.module_config.module_image is not None
            and self.module_config.module_image.path is not None
            and self.module_config.module_image.path.is_absolute()
            and not self.module_config.module_image.path.is_relative_to(
                self.path.parent
            )
        ):
            image_path = images_path / (
                "module" + self.module_config.module_image.path.suffix
            )

            shutil.copyfile(self.module_config.module_image.path, image_path)
            self.log.debug(
                f"Copied '{self.module_config.module_image.path}' to '{image_path}'."
            )

            self.module_config.module_image.path = image_path.relative_to(
                self.path.parent
            )

        if self.module_config.install_steps is None:
            return

        plugins: list[Plugin] = [
            plugin
            for install_step in self.module_config.install_steps.install_steps
            for group in install_step.optional_file_groups.groups
            for plugin in group.plugins.plugins
        ]

        for plugin in plugins:
            if plugin.image is not None and plugin.image.path.is_absolute():
                image_path = images_path / (plugin.name + plugin.image.path.suffix)

                shutil.copyfile(plugin.image.path, image_path)
                self.log.debug(f"Copied '{plugin.image.path}' to '{image_path}'.")

                plugin.image.path = image_path.relative_to(self.path.parent)

    def __include_required_files(self) -> None:
        if self.path is None:
            raise ValueError("FOMOD path is not set.")

        self.log.info("Including required install files...")

        files_path = self.path / "required_files"

        # TODO: Implement better way to clean up
        # if files_path.is_dir():
        #     shutil.rmtree(files_path)

        files_path.mkdir(parents=True, exist_ok=True)

        if self.module_config.required_install_files is None:
            return

        for install_file in self.module_config.required_install_files.files:
            if (
                install_file.source.is_absolute()
                and not install_file.source.is_relative_to(self.path.parent)
            ):
                file_path = files_path / install_file.source.name

                shutil.copyfile(install_file.source, file_path)
                self.log.debug(f"Copied '{install_file.source}' to '{file_path}'.")

                install_file.source = file_path.relative_to(self.path.parent)
            elif install_file.source.is_relative_to(self.path.parent):
                install_file.source = install_file.source.relative_to(self.path.parent)

        for install_folder in self.module_config.required_install_files.folders:
            if (
                install_folder.source.is_absolute()
                and not install_folder.source.is_relative_to(self.path.parent)
            ):
                folder_path = files_path / install_folder.source.name

                shutil.copytree(install_folder.source, folder_path, dirs_exist_ok=True)
                self.log.debug(f"Copied '{install_folder.source}' to '{folder_path}'.")

                install_folder.source = folder_path.relative_to(self.path.parent)
            elif install_folder.source.is_relative_to(self.path.parent):
                install_folder.source = install_folder.source.relative_to(
                    self.path.parent
                )

    def __include_conditional_files(self) -> None:
        if self.path is None:
            raise ValueError("FOMOD path is not set.")

        self.log.info("Including conditional install files...")

        files_path = self.path / "conditional_files"

        # TODO: Implement better way to clean up
        # if files_path.is_dir():
        #     shutil.rmtree(files_path)

        files_path.mkdir(parents=True, exist_ok=True)

        if self.module_config.conditional_file_installs is None:
            return

        for pattern in self.module_config.conditional_file_installs.patterns.patterns:
            for install_file in pattern.files.files:
                if (
                    install_file.source.is_absolute()
                    and not install_file.source.is_relative_to(self.path.parent)
                ):
                    file_path = files_path / install_file.source.name

                    shutil.copyfile(install_file.source, file_path)
                    self.log.debug(f"Copied '{install_file.source}' to '{file_path}'.")

                    install_file.source = file_path.relative_to(self.path.parent)
                elif install_file.source.is_relative_to(self.path.parent):
                    install_file.source = install_file.source.relative_to(
                        self.path.parent
                    )

            for install_folder in pattern.files.folders:
                if (
                    install_folder.source.is_absolute()
                    and not install_folder.source.is_relative_to(self.path.parent)
                ):
                    folder_path = files_path / install_folder.source.name

                    shutil.copytree(
                        install_folder.source, folder_path, dirs_exist_ok=True
                    )
                    self.log.debug(
                        f"Copied '{install_folder.source}' to '{folder_path}'."
                    )

                    install_folder.source = folder_path.relative_to(self.path.parent)
                elif install_folder.source.is_relative_to(self.path.parent):
                    install_folder.source = install_folder.source.relative_to(
                        self.path.parent
                    )

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
            info_path.write_bytes(self.info.dump())
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
            info=FomodInfo(name="default"),
            module_config=ModuleConfig(module_name=ModuleTitle(title="default")),
        )
