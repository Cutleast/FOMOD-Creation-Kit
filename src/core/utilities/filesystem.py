"""
Copyright (c) Cutleast
"""


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
