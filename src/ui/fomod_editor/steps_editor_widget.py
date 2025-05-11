"""
Copyright (c) Cutleast
"""

from typing import override

from .base_editor_widget import BaseEditorWidget


class StepsEditorWidget(BaseEditorWidget):
    """
    Widget class for editing the install steps (pages) of a FOMOD installer.
    """

    @override
    def validate(self) -> None: ...

    @override
    def save(self) -> None: ...
