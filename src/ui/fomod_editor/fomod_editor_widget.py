"""
Copyright (c) Cutleast
"""

from pathlib import Path
from typing import Optional, override

from PySide6.QtCore import Signal
from PySide6.QtWidgets import QTabWidget

from core.fomod.fomod import Fomod

from .info_editor_widget import InfoEditorWidget
from .module_config_editor_widget import ModuleConfigEditorWidget


class FomodEditorWidget(QTabWidget):
    """
    Widget for editing FOMOD installers.
    """

    changed = Signal(Fomod, bool)
    """
    Signal emitted when the FOMOD has changed.

    Args:
        Fomod: The FOMOD that has changed.
        bool: `True` if the FOMOD has changed, `False` if it was saved.
    """

    __current_fomod: Optional[Fomod] = None

    __info_editor_widget: Optional[InfoEditorWidget] = None
    __module_config_editor_widget: Optional[ModuleConfigEditorWidget] = None

    def __init__(self) -> None:
        super().__init__()

        self.setTabPosition(QTabWidget.TabPosition.West)
        self.tabBar().setExpanding(True)
        self.setObjectName("centered_tab")

    @override
    def clear(self) -> None:
        """
        Resets the FOMOD editor widget.
        """

        super().clear()

        self.__current_fomod = None
        self.__info_editor_widget = None
        self.__module_config_editor_widget = None

    def get_fomod(self) -> Optional[Fomod]:
        """
        Returns:
            Optional[Fomod]: The current FOMOD, or None if no FOMOD is set.
        """

        return self.__current_fomod

    def set_fomod(self, fomod: Fomod) -> None:
        """
        Sets the current FOMOD.

        Args:
            fomod (Fomod): The FOMOD to set.
        """

        self.clear()

        self.__current_fomod = fomod
        self.__init_info_editor_widget()
        self.__init_module_config_editor_widget()

        self.changed.emit(self.__current_fomod, False)

    def __init_info_editor_widget(self) -> None:
        if self.__current_fomod is None:
            raise ValueError("No FOMOD is set")

        self.__info_editor_widget = InfoEditorWidget(self.__current_fomod)
        self.__info_editor_widget.changed.connect(
            lambda: self.changed.emit(self.__current_fomod, True)
        )
        self.addTab(self.__info_editor_widget, self.tr("Info"))

    def __init_module_config_editor_widget(self) -> None:
        if self.__current_fomod is None:
            raise ValueError("No FOMOD is set")

        self.__module_config_editor_widget = ModuleConfigEditorWidget(
            self.__current_fomod
        )
        self.__module_config_editor_widget.changed.connect(
            lambda: self.changed.emit(self.__current_fomod, True)
        )
        self.addTab(self.__module_config_editor_widget, self.tr("Module Config"))

    def save(self, path: Optional[Path] = None) -> None:
        """
        Saves the current FOMOD installer (if any). Does nothing if no FOMOD is set.

        Args:
            path (Optional[Path], optional):
                The path to save the FOMOD installer to. Defaults to the FOMOD's current
                path.

        Raises:
            ValueError: if no FOMOD path is set
            ValidationError: if the FOMOD is invalid
        """

        if self.__current_fomod is None:
            return

        if self.__current_fomod.path is None and path is None:
            raise ValueError("No FOMOD path is set.")

        if path is not None:
            self.__current_fomod.path = path

        self.__validate()

        if self.__info_editor_widget is not None:
            self.__info_editor_widget.save()

        if self.__module_config_editor_widget is not None:
            self.__module_config_editor_widget.save()

        self.__current_fomod.save()
        self.changed.emit(self.__current_fomod, False)

    def __validate(self) -> None:
        if self.__info_editor_widget is not None:
            self.__info_editor_widget.validate()

        if self.__module_config_editor_widget is not None:
            self.__module_config_editor_widget.validate()
