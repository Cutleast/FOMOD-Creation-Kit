"""
Copyright (c) Cutleast
"""

import logging
import shutil
from pathlib import Path
from typing import Optional

from PySide6.QtCore import QObject

from core.fomod.module_config.file_item import FileItem
from core.fomod.module_config.file_list import FileList
from core.fomod.module_config.file_system.file_system_item import FileSystemItem
from core.fomod.module_config.folder_item import FolderItem
from core.fomod.module_config.image import Image
from core.utilities.filesystem import clean_fs_string, create_folder_list
from ui.widgets.loading_dialog import LoadingDialog

from .fomod import Fomod


class Finalizer(QObject):
    """
    Class that finalizes a FOMOD installer by copying all referenced files to its folder
    and making all references relative so that the FOMOD installer is ready to be packed
    in a zip file and distributed.
    """

    log: logging.Logger = logging.getLogger("Finalizer")

    MODULE_IMAGE_PATH = Path("ModuleImage")
    """Constant directing the path of the module image, relative to the FOMOD path."""

    IMAGES_PATH = Path("images")
    """Constant directing the path of the images, relative to the FOMOD path."""

    FILES_PATH = Path("files")
    """Constant directing the path of the files, relative to the FOMOD path."""

    INSTALL_STEP_FILES_PATH = FILES_PATH / "install_steps"
    """
    Constant directing the path of the install step files, relative to the FOMOD path.
    """

    REQUIRED_INSTALL_FILES_PATH = FILES_PATH / "required_install_files"
    """
    Constant directing the path of the required install files, relative to the FOMOD
    path.
    """

    CONDITIONAL_INSTALL_FILES_PATH = FILES_PATH / "conditional_install_files"
    """
    Constant directing the path of the conditional install files, relative to the FOMOD
    path.
    """

    def finalize(self, fomod: Fomod, ldialog: Optional[LoadingDialog] = None) -> None:
        """
        Finalizes the specified FOMOD installer.

        ### A finalized folder structure could look like this:
        ```
        fomod/
        ├─ ModuleConfig.xml
        ├─ info.xml
        ├─ ModuleImage/
        │  └─ example.png
        ├─ images/
        │  └─ Example Install Step/
        │     └─ Example Group/
        │        └─ Example Plugin/
        │           └─ example.jpg
        └─ files/
           ├─ install_steps/
           │  └─ Example Install Step/
           │     └─ Example Group/
           │        └─ Example Plugin/
           │           └─ example.esl
           ├─ required_install_files/
           │   ├─ interface/
           │   │  └─ translations/
           │   │     └─ example_english.txt
           │   └─ example.esp
           ├─ conditional_install_files.0/
           │   └─ example_patch.esp
           └─ conditional_install_files.1/
                └─ interface/
                    └─ translations/
                        └─ example_german.txt
        ```

        Args:
            fomod (Fomod): FOMOD to finalize.
            ldialog (Optional[LoadingDialog], optional):
                Optional loading dialog to display progress in. Defaults to None.

        Raises:
            ValueError: If the FOMOD path is not set.
        """

        if fomod.path is None:
            raise ValueError("FOMOD path is not set")

        self.log.info(f"Finalizing FOMOD '{fomod.info.name}' to '{fomod.path}'...")
        if ldialog is not None:
            ldialog.updateProgress(text1=self.tr("Finalizing FOMOD..."))

        self.__process_images(fomod, fomod.path, ldialog)
        self.__process_files(fomod, fomod.path, ldialog)

        self.log.info(f"Finalized FOMOD '{fomod.info.name}' to '{fomod.path}'")

    def __process_images(
        self, fomod: Fomod, fomod_path: Path, ldialog: Optional[LoadingDialog] = None
    ) -> None:
        """
        Processes the FOMOD's images by copying them to a subfolder of the FOMOD path.

        Args:
            fomod (Fomod): FOMOD to process
            fomod_path (Path): Path of the FOMOD
            ldialog (Optional[LoadingDialog], optional):
                Optional loading dialog to display progress in. Defaults to None.
        """

        from send2trash import send2trash

        self.log.info("Processing images...")
        if ldialog is not None:
            ldialog.updateProgress(text2=self.tr("Processing images..."), show2=True)

        images_path: Path = fomod_path / Finalizer.IMAGES_PATH

        # list to keep track of referenced images - all other files will be deleted at
        # the end
        image_files: list[Path] = []

        if (
            fomod.module_config.module_image is not None
            and fomod.module_config.module_image.path is not None
        ):
            fomod.module_config.module_image.path = self.__process_file(
                fomod.module_config.module_image.path,
                str(Finalizer.MODULE_IMAGE_PATH),
                fomod_path,
            )
            image_files.append(fomod.module_config.module_image.path)

        if fomod.module_config.install_steps is not None:
            plugin_images: list[tuple[str, Image]] = [
                (
                    f"/{clean_fs_string(install_step.name)}/{clean_fs_string(group.name)}"
                    f"/{clean_fs_string(plugin.name)}",
                    plugin.image,
                )
                for install_step in fomod.module_config.install_steps.install_steps
                for group in install_step.optional_file_groups.groups
                for plugin in group.plugins.plugins
                if plugin.image is not None
            ]

            for name, image in plugin_images:
                image.path = self.__process_file(
                    image.path,
                    str(Finalizer.IMAGES_PATH) + name,
                    fomod_path,
                )
                image_files.append(image.path)

        self.log.info(f"Processed {len(image_files)} image(s).")

        for file in images_path.rglob("*"):
            if (
                file.is_file()
                and file.relative_to(fomod_path.parent) not in image_files
            ):
                try:
                    send2trash(file)
                    self.log.info(f"Moved file '{file}' to trash bin.")
                except Exception as ex:
                    self.log.warning(
                        f"Failed to move '{file}' to trash bin: {ex}", exc_info=ex
                    )

    def __process_files(
        self, fomod: Fomod, fomod_path: Path, ldialog: Optional[LoadingDialog] = None
    ) -> None:
        """
        Processes the installation files by copying them to a subfolder of the FOMOD
        path.

        Args:
            fomod (Fomod): FOMOD to process
            fomod_path (Path): Path of the FOMOD
            ldialog (Optional[LoadingDialog], optional):
                Optional loading dialog to display progress in. Defaults to None.
        """

        from send2trash import send2trash

        self.log.info("Processing files...")

        if fomod.module_config.required_install_files is not None:
            self.__process_file_list(
                fomod.module_config.required_install_files,
                fomod_path,
                str(Finalizer.REQUIRED_INSTALL_FILES_PATH),
                ldialog,
            )

        elif (fomod_path / Finalizer.REQUIRED_INSTALL_FILES_PATH).is_dir():
            send2trash(fomod_path / Finalizer.REQUIRED_INSTALL_FILES_PATH)
            self.log.info(
                "Moved obsolete folder 'required_install_files' folder to trash bin."
            )

        if fomod.module_config.conditional_file_installs is not None:
            for p, pattern in enumerate(
                fomod.module_config.conditional_file_installs.patterns.patterns
            ):
                self.__process_file_list(
                    pattern.files,
                    fomod_path,
                    str(Finalizer.CONDITIONAL_INSTALL_FILES_PATH.with_suffix(f".{p}")),
                    ldialog,
                )

            self.log.info(
                "Processed "
                f"{len(fomod.module_config.conditional_file_installs.patterns.patterns)}"
                " conditional file install(s)."
            )

        elif obsolete_conditional_files := list(
            fomod_path.glob("conditional_install_files.*")
        ):
            for folder in obsolete_conditional_files:
                if not folder.is_dir():
                    continue

                send2trash(folder)
                self.log.info(f"Moved obsolete folder '{folder}' to trash bin.")

        if fomod.module_config.install_steps is not None:
            plugin_files: list[tuple[str, FileList]] = [
                (
                    f"/{clean_fs_string(install_step.name)}/{clean_fs_string(group.name)}"
                    f"/{clean_fs_string(plugin.name)}",
                    plugin.files,
                )
                for install_step in fomod.module_config.install_steps.install_steps
                for group in install_step.optional_file_groups.groups
                for plugin in group.plugins.plugins
                if plugin.files is not None
            ]

            for name, files in plugin_files:
                self.__process_file_list(
                    files,
                    fomod_path,
                    str(Finalizer.INSTALL_STEP_FILES_PATH) + name,
                    ldialog,
                )

        elif (fomod_path / "install_steps").is_dir():
            send2trash(fomod_path / "install_steps")
            self.log.info("Moved obsolete folder 'install_steps' folder to trash bin.")

    def __process_file_list(
        self,
        file_list: FileList,
        fomod_path: Path,
        folder_name: str,
        ldialog: Optional[LoadingDialog] = None,
    ) -> None:
        """
        Processes a FileList object by copying its files to a subfolder of the FOMOD
        path.

        Args:
            file_list (FileList): FileList to process.
            fomod_path (Path): Path of the FOMOD.
            folder_name (str):
                Name of the subdirectory in the files directory to copy the files to.
            ldialog (Optional[LoadingDialog], optional):
                Optional loading dialog to display progress in. Defaults to None.
        """

        from send2trash import send2trash

        self.log.info(f"Processing '{folder_name}'...")
        if ldialog is not None:
            ldialog.updateProgress(
                text2=self.tr("Processing '{0}'...").format(folder_name), show2=True
            )

        destination: Path = fomod_path / folder_name
        destination.mkdir(parents=True, exist_ok=True)

        items: list[FileSystemItem] = [
            item for item in file_list.files + file_list.folders
        ]

        # Used to track which files are referenced and which should be cleaned later
        referenced_files: list[Path] = []

        for i, item in enumerate(items):
            self.log.info(f"Processing '{folder_name}' ({i}/{len(items)})...")
            if ldialog is not None:
                ldialog.updateProgress(
                    value2=i,
                    max2=len(items),
                    text2=self.tr("Processing '{0}'...").format(folder_name)
                    + f" ({i}/{len(items)})",
                    text3=str(item.source),
                    show3=True,
                )

            if isinstance(item, FileItem):
                item.source = self.__process_file(item.source, folder_name, fomod_path)
                referenced_files.append(item.source)

            elif isinstance(item, FolderItem):
                copied_files: list[Path]
                item.source, copied_files = self.__process_folder(
                    item.source, folder_name, fomod_path
                )
                referenced_files.extend([item.source / f for f in copied_files])

            else:
                self.log.error(
                    f"Failed to process '{item.source}': Unknown type '{type(item)}'."
                )

        self.log.info(f"Processed {len(items)} item(s).")

        for file in destination.rglob("*"):
            if (
                file.is_file()
                and file.relative_to(fomod_path.parent) not in referenced_files
            ):
                try:
                    send2trash(file)
                    self.log.info(f"Moved file '{file}' to trash bin.")
                except Exception as ex:
                    self.log.warning(
                        f"Failed to move '{file}' to trash bin: {ex}", exc_info=ex
                    )

    def __process_file(self, source: Path, name: str, fomod_path: Path) -> Path:
        """
        Copies the specified file to a subfolder of the specified name in the FOMOD path.
        Does nothing if the specified source path is already absolute and within the
        FOMOD path and just returns its path relative to the parent of the FOMOD path.

        Args:
            source (Path): Source file to copy
            name (str): Name of the subfolder/directory
            fomod_path (Path): Path of the FOMOD installer

        Returns:
            Path: Path of the copied file relative to the parent of the FOMOD path
        """

        if not Finalizer.is_path_outside_of_fomod(source, fomod_path):
            return (
                source.relative_to(fomod_path.parent)
                if source.is_relative_to(fomod_path)
                else source
            )

        new_file_path: Path = fomod_path / name / source.name
        new_file_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, new_file_path)
        self.log.info(f"Copied '{source}' to '{new_file_path}'.")

        return new_file_path.relative_to(fomod_path.parent)

    def __process_folder(
        self, source: Path, name: str, fomod_path: Path
    ) -> tuple[Path, list[Path]]:
        """
        Copies the specified folder to a subfolder of the specified name in the FOMOD
        path. Does nothing if the specified source path is already absolute and within
        the FOMOD path and just returns its path relative to the parent of the FOMOD
        path and a list of the files in the folder.

        Args:
            source (Path): Source folder to copy
            name (str): Name of the subfolder/directory
            fomod_path (Path): Path of the FOMOD installer

        Returns:
            tuple[Path, list[Path]]:
                Path of the copied folder relative to the parent and a list of the copied
                files
        """

        if not Finalizer.is_path_outside_of_fomod(source, fomod_path):
            return (
                source.relative_to(fomod_path.parent)
                if source.is_relative_to(fomod_path)
                else source
            ), create_folder_list(source)

        new_folder_path: Path = fomod_path / name / source.name
        new_folder_path.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, new_folder_path)
        self.log.info(f"Copied '{source}' to '{new_folder_path}'.")

        return new_folder_path.relative_to(fomod_path.parent), create_folder_list(
            new_folder_path
        )

    @staticmethod
    def is_path_outside_of_fomod(path: Path, fomod_path: Path) -> bool:
        """
        Checks if the specified path lies outside of the specified FOMOD path.

        This is True when:
        - the path is absolute
        - and the path is not relative to the parent of the specified FOMOD path

        Args:
            path (Path): Path to check
            fomod_path (Path): Path of the FOMOD installer

        Returns:
            bool: True if the path lies outside of the FOMOD path
        """

        return path.is_absolute() and not path.is_relative_to(fomod_path.parent)
