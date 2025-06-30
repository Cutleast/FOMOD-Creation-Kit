"""
Copyright (c) Cutleast
"""

from typing import Optional, Sequence, override

import PySide6.QtCore as qtc
import PySide6.QtWidgets as qtw


class AutoCompleteCombobox(qtw.QComboBox):
    """
    Preconfigured QComboBox that supports auto-completion from a given set of items.
    """

    def __init__(self):
        super().__init__()

        self.setEditable(True)
        self.setContentsMargins(0, 0, 0, 0)

    @override
    def addItems(self, texts: Sequence[str]) -> None:
        super().addItems(texts)

        completer = qtw.QCompleter(texts)
        completer.popup().setObjectName("completer_popup")
        completer.setCaseSensitivity(qtc.Qt.CaseSensitivity.CaseInsensitive)
        completer.setCompletionMode(qtw.QCompleter.CompletionMode.PopupCompletion)
        self.setCompleter(completer)

    @override
    def setPlaceholderText(self, placeholderText: str) -> None:
        lineEdit: Optional[qtw.QLineEdit] = self.lineEdit()
        if lineEdit is not None:
            lineEdit.setPlaceholderText(placeholderText)

        return super().setPlaceholderText(placeholderText)
