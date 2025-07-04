"""
Copyright (c) Cutleast
"""

import logging
from pathlib import Path

from PySide6.QtCore import QObject, Signal


class History(QObject):
    """
    Class holding a history of the recent opened FOMOD installers and their paths.
    """

    changed = Signal()
    """Signal that gets emitted when the history changes or gets cleared."""

    path: Path
    """
    Path to the history.txt containing the paths of the recent opened FOMOD installers.
    """

    log: logging.Logger = logging.getLogger("History")

    def __init__(self, data_path: Path) -> None:
        """
        Args:
            data_path (Path): Path to the app's data folder.
        """

        self.path = data_path / "history.txt"

    @property
    def recent_fomods(self) -> list[Path]:
        """
        A list of the recently opened FOMOD installers. List is ordered last before
        first.
        """

        if not self.path.is_file():
            return []

        return [
            Path(line.strip())
            for line in self.path.read_text(encoding="utf8").splitlines()
        ]

    def add(self, fomod_path: Path) -> None:
        """
        Adds the specified FOMOD path to the history. If it is already in the list,
        this moves it to the bottom.

        Args:
            fomod_path (Path): Path to the FOMOD to add to the history.
        """

        fomods: list[Path] = self.recent_fomods

        if fomod_path in fomods:
            fomods.remove(fomod_path)
        fomods.append(fomod_path)

        self.__save(fomods)
        self.log.debug(f"Added '{fomod_path}' to history.")

    def __save(self, fomods: list[Path]) -> None:
        """
        Saves the history by writing the specified paths to the history.txt file.

        Args:
            fomods (list[Path]): List of paths to save to the history.txt file.
        """

        self.path.write_text("\n".join(str(f) for f in fomods), encoding="utf8")
        self.log.debug(f"Saved history with {len(fomods)} entries.")

    def clear(self) -> None:
        """
        Clears the history by deleting the history.txt file.
        """

        self.path.unlink(missing_ok=True)
        self.log.debug("Cleared history.")
