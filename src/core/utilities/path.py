"""
Copyright (c) Cutleast
"""

from pathlib import Path
from typing import Optional


def get_joined_path_if_relative(path: Path, base_path: Optional[Path] = None) -> Path:
    """
    Joins the specified path to the base path if the path is relative.
    Does nothing if the path is absolute or if the base path is None.

    Args:
        path (Path): The path to join to the base path.
        base_path (Optional[Path], optional):
            The base path. Defaults to None.

    Returns:
        Path: The joined path.
    """

    if not path.is_absolute() and base_path is not None:
        return base_path / path

    return path
