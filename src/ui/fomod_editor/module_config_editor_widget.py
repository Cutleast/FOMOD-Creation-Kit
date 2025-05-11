"""
Copyright (c) Cutleast
"""

from typing import override

from .base_editor_widget import BaseEditorWidget


class ModuleConfigEditorWidget(BaseEditorWidget):
    """
    Widget class for editing the module configuration of a FOMOD installer.
    """

    @override
    def validate(self) -> None: ...

    @override
    def save(self) -> None: ...
