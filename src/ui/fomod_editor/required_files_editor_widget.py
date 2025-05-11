"""
Copyright (c) Cutleast
"""

from typing import override

from .base_editor_widget import BaseEditorWidget


class RequiredFilesEditorWidget(BaseEditorWidget):
    """
    Widget class for editing the required install files of a FOMOD installer.
    """

    @override
    def validate(self) -> None: ...

    @override
    def save(self) -> None: ...
