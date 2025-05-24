"""
Copyright (c) Cutleast
"""

from pathlib import Path
from typing import Optional, override

import qtawesome as qta
from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QTransform
from PySide6.QtWidgets import QTabWidget

from core.fomod.fomod import Fomod
from core.fomod.module_config.condition.conditional_file_install_list import (
    ConditionalFileInstallList,
)
from core.fomod.module_config.dependency.composite_dependency import CompositeDependency
from core.fomod.module_config.file_list import FileList
from core.fomod.module_config.step_list import StepList
from ui.utilities.icon_provider import get_icon_for_palette

from .conditional_files_editor_widget import ConditionalFilesEditorWidget
from .dependency_editor_widget import DependencyEditorWidget
from .info_editor_widget import InfoEditorWidget
from .required_files_editor_widget import RequiredFilesEditorWidget
from .steps_editor_widget import StepsEditorWidget


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

    TAB_ICON_SIZE: int = 24
    """Size of the tab icons in pixels."""

    __current_fomod: Optional[Fomod] = None

    __info_editor_widget: Optional[InfoEditorWidget] = None
    __dependency_editor_widget: Optional[DependencyEditorWidget] = None
    __required_files_editor_widget: Optional[RequiredFilesEditorWidget] = None
    __steps_editor_widget: Optional[StepsEditorWidget] = None
    __conditional_files_editor_widget: Optional[ConditionalFilesEditorWidget] = None

    def __init__(self) -> None:
        super().__init__()

        self.setTabPosition(QTabWidget.TabPosition.West)
        self.tabBar().setExpanding(True)
        self.setObjectName("icon_bar")
        self.tabBar().setObjectName("icon_bar")
        self.tabBar().setIconSize(
            QSize(FomodEditorWidget.TAB_ICON_SIZE, FomodEditorWidget.TAB_ICON_SIZE)
        )

    @override
    def clear(self) -> None:
        """
        Resets the FOMOD editor widget.
        """

        super().clear()

        self.__current_fomod = None
        self.__info_editor_widget = None
        self.__dependency_editor_widget = None
        self.__steps_editor_widget = None
        self.__conditional_files_editor_widget = None

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
        self.__init_dependency_editor_widget()
        self.__init_required_files_editor_widget()
        self.__init_steps_editor_widget()
        self.__init_conditional_files_editor_widget()

        self.changed.emit(self.__current_fomod, False)

    def __init_info_editor_widget(self) -> None:
        if self.__current_fomod is None:
            raise ValueError("No FOMOD is set")

        self.__info_editor_widget = InfoEditorWidget(self.__current_fomod)
        self.__info_editor_widget.changed.connect(
            lambda: self.changed.emit(self.__current_fomod, True)
        )

        i: int = self.addTab(
            self.__info_editor_widget,
            get_icon_for_palette("quick_reference", self.palette())
            .pixmap(FomodEditorWidget.TAB_ICON_SIZE, FomodEditorWidget.TAB_ICON_SIZE)
            .transformed(
                QTransform().rotate(90), Qt.TransformationMode.SmoothTransformation
            ),
            "",
        )
        self.setTabToolTip(i, self.tr("Info"))

    def __init_dependency_editor_widget(self) -> None:
        if self.__current_fomod is None:
            raise ValueError("No FOMOD is set")

        self.__dependency_editor_widget = DependencyEditorWidget(
            self.__current_fomod.module_config.module_dependencies
            or CompositeDependency()
        )
        self.__dependency_editor_widget.changed.connect(
            lambda: self.changed.emit(self.__current_fomod, True)
        )

        i: int = self.addTab(
            self.__dependency_editor_widget,
            qta.icon("fa6s.list-check", color=self.palette().text().color())
            .pixmap(FomodEditorWidget.TAB_ICON_SIZE, FomodEditorWidget.TAB_ICON_SIZE)
            .transformed(
                QTransform().rotate(90), Qt.TransformationMode.SmoothTransformation
            ),
            "",
        )
        self.setTabToolTip(i, self.tr("Module Dependencies"))

    def __init_required_files_editor_widget(self) -> None:
        if self.__current_fomod is None:
            raise ValueError("No FOMOD is set")

        self.__required_files_editor_widget = RequiredFilesEditorWidget(
            self.__current_fomod.module_config.required_install_files or FileList()
        )
        self.__required_files_editor_widget.changed.connect(
            lambda: self.changed.emit(self.__current_fomod, True)
        )

        i: int = self.addTab(
            self.__required_files_editor_widget,
            qta.icon("mdi6.file-check", color=self.palette().text().color())
            .pixmap(FomodEditorWidget.TAB_ICON_SIZE, FomodEditorWidget.TAB_ICON_SIZE)
            .transformed(
                QTransform().rotate(90), Qt.TransformationMode.SmoothTransformation
            ),
            "",
        )
        self.setTabToolTip(i, self.tr("Required files to install"))

    def __init_steps_editor_widget(self) -> None:
        if self.__current_fomod is None:
            raise ValueError("No FOMOD is set")

        self.__steps_editor_widget = StepsEditorWidget(
            self.__current_fomod.module_config.install_steps
            or StepList(install_steps=[])
        )
        self.__steps_editor_widget.changed.connect(
            lambda: self.changed.emit(self.__current_fomod, True)
        )

        i: int = self.addTab(
            self.__steps_editor_widget,
            qta.icon("mdi6.book-open-page-variant", color=self.palette().text().color())
            .pixmap(FomodEditorWidget.TAB_ICON_SIZE, FomodEditorWidget.TAB_ICON_SIZE)
            .transformed(
                QTransform().rotate(90), Qt.TransformationMode.SmoothTransformation
            ),
            "",
        )
        self.setTabToolTip(i, self.tr("Installation steps (pages)"))

    def __init_conditional_files_editor_widget(self) -> None:
        if self.__current_fomod is None:
            raise ValueError("No FOMOD is set")

        self.__conditional_files_editor_widget = ConditionalFilesEditorWidget(
            self.__current_fomod.module_config.conditional_file_installs
            or ConditionalFileInstallList(patterns=[])
        )
        self.__conditional_files_editor_widget.changed.connect(
            lambda: self.changed.emit(self.__current_fomod, True)
        )

        i: int = self.addTab(
            self.__conditional_files_editor_widget,
            qta.icon("fa6s.file-circle-question", color=self.palette().text().color())
            .pixmap(FomodEditorWidget.TAB_ICON_SIZE, FomodEditorWidget.TAB_ICON_SIZE)
            .transformed(
                QTransform().rotate(90), Qt.TransformationMode.SmoothTransformation
            ),
            "",
        )
        self.setTabToolTip(i, self.tr("Conditional files to install"))

    def save(
        self,
        path: Optional[Path] = None,
        validate_xml: bool = True,
        encoding: str = "utf-8",
    ) -> None:
        """
        Saves the current FOMOD installer (if any). Does nothing if no FOMOD is set.

        Args:
            path (Optional[Path], optional):
                The path to save the FOMOD installer to. Defaults to the FOMOD's current
                path.
            validate_xml (bool, optional):
                Whether to validate the XML files before saving. Defaults to True.
            encoding (str, optional):
                The encoding to use for the XML files. Defaults to "utf-8".

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

        self.validate()

        if self.__info_editor_widget is not None:
            self.__info_editor_widget.save()

        if self.__dependency_editor_widget is not None:
            self.__current_fomod.module_config.module_dependencies = (
                self.__dependency_editor_widget.save()
            )

        if self.__required_files_editor_widget is not None:
            self.__current_fomod.module_config.required_install_files = (
                self.__required_files_editor_widget.save()
            )

        if self.__steps_editor_widget is not None:
            self.__current_fomod.module_config.install_steps = (
                self.__steps_editor_widget.save()
            )

        if self.__conditional_files_editor_widget is not None:
            self.__current_fomod.module_config.conditional_file_installs = (
                self.__conditional_files_editor_widget.save()
            )

        self.__current_fomod.save(validate_xml, encoding)
        self.changed.emit(self.__current_fomod, False)

    def validate(self) -> None:
        """
        Validates the current FOMOD.

        Raises:
            ValidationError: if the FOMOD is invalid
        """

        if self.__info_editor_widget is not None:
            self.__info_editor_widget.validate()

        if self.__dependency_editor_widget is not None:
            self.__dependency_editor_widget.validate()

        if self.__required_files_editor_widget is not None:
            self.__required_files_editor_widget.validate()

        if self.__steps_editor_widget is not None:
            self.__steps_editor_widget.validate()

        if self.__conditional_files_editor_widget is not None:
            self.__conditional_files_editor_widget.validate()
