"""
Copyright (c) Cutleast
"""

from PySide6.QtCore import QTranslator
from PySide6.QtWidgets import QApplication
from pytestqt.qtbot import QtBot

from core.utilities.localisation import Language
from tests.base_test import BaseTest


class TestLocalisation(BaseTest):
    """
    Tests `core.utilities.localisation`.
    """

    def test_all_langs_can_be_loaded(self, qtbot: QtBot) -> None:
        """
        Tests that all required .qm files are bundled and can be loaded by the
        QTranslator.
        """

        # given
        qm_files: list[str] = [
            f":/loc/{lang.value}.qm"
            for lang in Language
            if lang not in [Language.System, Language.English]
        ]
        translator = QTranslator(QApplication.instance())

        # then
        for qm_file in qm_files:
            assert translator.load(qm_file), (
                f"Failed to load '{qm_file}'! Make sure to add "
                f'"<file>{qm_file.removeprefix(":/")}</file>" to ./res/resources.qrc!'
            )
