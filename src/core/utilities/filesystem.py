"""
Copyright (c) Cutleast
"""

import os
from pathlib import Path


def create_folder_list(folder: Path) -> list[Path]:
    """
    Creates a list of all files in all subdirectories of a folder.

    Args:
        folder (Path): Folder to get list of files of.

    Returns:
        list[Path]: List of relative file paths from folder and all subdirectories.
    """

    return [item.relative_to(folder) for item in folder.glob("**/*") if item.is_file()]


def get_common_files(
    files1: list[str], files2: list[str], ignore_case: bool = True
) -> list[str]:
    """
    Gets common files between two lists.

    Args:
        files1 (list[str]): First list of files
        files2 (list[str]): Second list of files
        ignore_case (bool, optional): Toggles whether to ignore case. Defaults to True.

    Returns:
        list[str]: List of common files
    """

    return [
        file
        for file in files1
        if file in files2
        or (file.lower() in [f.lower() for f in files2] and ignore_case)
    ]


def clean_fs_string(text: str) -> str:
    """
    Cleans a string from illegal path characters like ':', '?' or '/'.
    Also removes leading and trailing whitespace and trailing '.'.

    Args:
        text (str): the string to be cleaned.

    Returns:
        str: A cleaned-up string.
    """

    illegal_chars: str = r"""<>\/|*?":"""
    output: str = "".join([c for c in text if c not in illegal_chars])
    output = output.strip().rstrip(".")

    return output


def open_in_explorer(path: Path) -> None:
    """
    Opens the specified path in the Windows Explorer.
    Opens the parent folder and selects the item if the specified path
    is a file otherwise it just opens the folder.

    Args:
        path (Path): The path to open.
    """

    if path.is_dir():
        os.startfile(path)
    else:
        os.system(f'explorer.exe /select,"{path}"')
