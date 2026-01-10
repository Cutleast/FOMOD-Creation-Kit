"""
Copyright (c) Cutleast
"""

from core.utilities.reference_dict import ReferenceDict

from .base_editor_widget import BaseEditorWidget, FomodItem
from .editor_window import EditorWindow


class EditorWindowService:
    """
    Singleton class for managing editor windows.
    """

    __editor_windows: ReferenceDict[FomodItem, EditorWindow] = ReferenceDict()
    """Dictionary mapping FOMOD items to open editor windows."""

    @classmethod
    def provide_editor_window[T: BaseEditorWidget](
        cls, editor_widget: T, validate_on_init: bool = False
    ) -> tuple[EditorWindow[T], bool]:
        """
        Creates or returns an existing editor window for the given editor widget.

        Args:
            editor_widget (T): FOMOD editor widget to wrap in a dialog.
            validate_on_init (bool, optional):
                Whether to validate (and enable the save button) on initialization.
                Defaults to False.

        Returns:
            tuple[EditorWindow[T], bool]:
                Editor window for the given editor widget and whether it was created.
        """

        item: FomodItem = editor_widget.get_item()

        if item in cls.__editor_windows:
            return cls.__editor_windows[item], False

        window = EditorWindow(editor_widget, validate_on_init)
        window.destroyed.connect(lambda: cls.__editor_windows.pop(item))
        cls.__editor_windows[item] = window
        return window, True
