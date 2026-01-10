"""
Copyright (c) Cutleast
"""

from typing import override

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QGridLayout,
    QLabel,
    QLineEdit,
    QTabWidget,
    QWidget,
)

from core.fomod.module_config.dependency.composite_dependency import CompositeDependency
from core.fomod.module_config.dependency.file_dependency import FileDependency
from core.fomod.module_config.dependency.flag_dependency import FlagDependency
from core.fomod.module_config.dependency.version_dependency import VersionDependency
from core.fomod_editor.exceptions import EmptyError, SpecificValidationError
from ui.widgets.tree_widget_editor import TreeWidgetEditor

from ..base_editor_widget import BaseEditorWidget
from ..editor_window import EditorWindow
from ..editor_window_service import EditorWindowService
from .file_dependency_editor_widget import FileDependencyEditorWidget
from .flag_dependency_editor_widget import FlagDependencyEditorWidget


class DependencyGroupEditorWidget(BaseEditorWidget[CompositeDependency]):
    """
    Widget for editing/creating a dependency group.
    """

    __tab_widget: QTabWidget
    __files_tree_widget_editor: TreeWidgetEditor[FileDependency]
    __flags_tree_widget_editor: TreeWidgetEditor[FlagDependency]

    __game_version_checkbox: QCheckBox
    __game_version_entry: QLineEdit
    __fomm_version_checkbox: QCheckBox
    __fomm_version_entry: QLineEdit

    __dependencies_tree_widget_editor: TreeWidgetEditor[CompositeDependency]

    @override
    def _post_init(self) -> None:
        self.__files_tree_widget_editor.changed.connect(self.changed.emit)
        self.__files_tree_widget_editor.onAdd.connect(self.__add_file_dependency)
        self.__files_tree_widget_editor.onEdit.connect(self.__edit_file_dependency)

        self.__flags_tree_widget_editor.changed.connect(self.changed.emit)
        self.__flags_tree_widget_editor.onAdd.connect(self.__add_flag_dependency)
        self.__flags_tree_widget_editor.onEdit.connect(self.__edit_flag_dependency)

        self.__game_version_checkbox.stateChanged.connect(lambda _: self.changed.emit())
        self.__game_version_checkbox.stateChanged.connect(
            self.__game_version_entry.setEnabled
        )
        self.__game_version_entry.textChanged.connect(lambda _: self.changed.emit())
        self.__fomm_version_checkbox.stateChanged.connect(lambda _: self.changed.emit())
        self.__fomm_version_checkbox.stateChanged.connect(
            self.__fomm_version_entry.setEnabled
        )
        self.__fomm_version_entry.textChanged.connect(lambda _: self.changed.emit())

        self.__dependencies_tree_widget_editor.changed.connect(self.changed.emit)
        self.__dependencies_tree_widget_editor.onAdd.connect(self.__add_dependency)
        self.__dependencies_tree_widget_editor.onEdit.connect(self.__edit_dependency)

    @override
    @classmethod
    def get_display_name(cls) -> str:
        return QApplication.translate(
            "DependencyGroupEditorWidget", "Edit dependency group..."
        )

    @override
    def _init_ui(self) -> None:
        super()._init_ui()

        self.__tab_widget = QTabWidget()
        self.__tab_widget.setObjectName("centered_tab")
        self.__tab_widget.tabBar().setDocumentMode(True)
        self.__tab_widget.tabBar().setExpanding(True)
        self._vlayout.addWidget(self.__tab_widget)

        self.__init_files_tab()
        self.__init_flags_tab()
        self.__init_versions_tab()
        self.__init_dependencies_tab()

        self.__set_initial_tab()

    def __set_initial_tab(self) -> None:
        # select the first non-empty tab
        if self._item.dependencies:
            self.__tab_widget.setCurrentIndex(3)

        if self._item.game_dependency or self._item.fomm_dependency:
            self.__tab_widget.setCurrentIndex(2)

        if self._item.flag_dependencies:
            self.__tab_widget.setCurrentIndex(1)

        if self._item.file_dependencies:
            self.__tab_widget.setCurrentIndex(0)

    def __init_files_tab(self) -> None:
        self.__files_tree_widget_editor = TreeWidgetEditor(
            self._item.file_dependencies.copy()
        )
        self.__tab_widget.addTab(self.__files_tree_widget_editor, self.tr("Files"))

    def __add_file_dependency(self) -> None:
        file_dependency = FileDependency(file="", state=FileDependency.State.Active)
        window: EditorWindow[FileDependencyEditorWidget] = (
            EditorWindowService.provide_editor_window(
                FileDependencyEditorWidget(
                    file_dependency, self._fomod_path, self._flag_names_supplier
                ),
                validate_on_init=True,
            )[0]
        )
        window.saved.connect(
            lambda: self.__files_tree_widget_editor.addItem(file_dependency)
        )
        window.show_and_activate()

    def __edit_file_dependency(self, item: FileDependency) -> None:
        window: EditorWindow[FileDependencyEditorWidget] = (
            EditorWindowService.provide_editor_window(
                FileDependencyEditorWidget(
                    item, self._fomod_path, self._flag_names_supplier
                )
            )[0]
        )
        window.saved.connect(lambda: self.__files_tree_widget_editor.updateItem(item))
        window.show_and_activate()

    def __init_flags_tab(self) -> None:
        self.__flags_tree_widget_editor = TreeWidgetEditor(
            self._item.flag_dependencies.copy()
        )
        self.__tab_widget.addTab(self.__flags_tree_widget_editor, self.tr("Flags"))

    def __add_flag_dependency(self) -> None:
        flag_dependency = FlagDependency(flag="", value="")
        window: EditorWindow[FlagDependencyEditorWidget] = (
            EditorWindowService.provide_editor_window(
                FlagDependencyEditorWidget(
                    flag_dependency, self._fomod_path, self._flag_names_supplier
                ),
                validate_on_init=True,
            )[0]
        )
        window.saved.connect(
            lambda: self.__flags_tree_widget_editor.addItem(flag_dependency)
        )
        window.show_and_activate()

    def __edit_flag_dependency(self, item: FlagDependency) -> None:
        window: EditorWindow[FlagDependencyEditorWidget] = (
            EditorWindowService.provide_editor_window(
                FlagDependencyEditorWidget(
                    item, self._fomod_path, self._flag_names_supplier
                )
            )[0]
        )
        window.saved.connect(lambda: self.__flags_tree_widget_editor.updateItem(item))
        window.show_and_activate()

    def __init_versions_tab(self) -> None:
        versions_tab_widget = QWidget()
        self.__tab_widget.addTab(versions_tab_widget, self.tr("Versions"))

        glayout = QGridLayout()
        glayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        versions_tab_widget.setLayout(glayout)

        self.__game_version_checkbox = QCheckBox(self.tr("Game Version"))
        self.__game_version_checkbox.setChecked(self._item.game_dependency is not None)
        glayout.addWidget(self.__game_version_checkbox, 0, 0)

        self.__game_version_entry = QLineEdit()
        self.__game_version_entry.setEnabled(self._item.game_dependency is not None)
        self.__game_version_entry.setPlaceholderText(
            self.tr('eg. "1.6.1170.0" or "1.5.97"')
        )
        if self._item.game_dependency is not None:
            self.__game_version_entry.setText(self._item.game_dependency.version)
        glayout.addWidget(self.__game_version_entry, 0, 1)

        game_version_help_label = QLabel(
            self.tr(
                "When specified, the game must have the version above for this "
                "dependency to be fulfilled."
            )
        )
        game_version_help_label.setWordWrap(True)
        glayout.addWidget(game_version_help_label, 1, 1)

        glayout.addWidget(QLabel(), 2, 0)

        self.__fomm_version_checkbox = QCheckBox(self.tr("FOMM Version"))
        self.__fomm_version_checkbox.setChecked(self._item.fomm_dependency is not None)
        glayout.addWidget(self.__fomm_version_checkbox, 3, 0)

        self.__fomm_version_entry = QLineEdit()
        self.__fomm_version_entry.setEnabled(self._item.fomm_dependency is not None)
        if self._item.fomm_dependency is not None:
            self.__fomm_version_entry.setText(self._item.fomm_dependency.version)
        glayout.addWidget(self.__fomm_version_entry, 3, 1)

        fomm_version_help_label = QLabel(
            self.tr(
                "This seems to be an outdated parameter specifying the minimum "
                "required version of the Fallout Mod Manager. It is unsure whether this "
                "affects anything or is considered by the installing mod manager."
            )
        )
        fomm_version_help_label.setWordWrap(True)
        glayout.addWidget(fomm_version_help_label, 4, 1)

    def __init_dependencies_tab(self) -> None:
        self.__dependencies_tree_widget_editor = TreeWidgetEditor(
            self._item.dependencies.copy()
        )
        self.__tab_widget.addTab(
            self.__dependencies_tree_widget_editor, self.tr("Dependencies")
        )

    def __add_dependency(self) -> None:
        from .composite_dependency_editor_widget import CompositeDependencyEditorWidget

        dependency = CompositeDependency()
        window: EditorWindow[CompositeDependencyEditorWidget] = (
            EditorWindowService.provide_editor_window(
                CompositeDependencyEditorWidget(
                    dependency, self._fomod_path, self._flag_names_supplier
                ),
                validate_on_init=True,
            )[0]
        )
        window.saved.connect(
            lambda: self.__dependencies_tree_widget_editor.addItem(dependency)
        )
        window.show_and_activate()

    def __edit_dependency(self, item: CompositeDependency) -> None:
        from .composite_dependency_editor_widget import CompositeDependencyEditorWidget

        window: EditorWindow[CompositeDependencyEditorWidget] = (
            EditorWindowService.provide_editor_window(
                CompositeDependencyEditorWidget(
                    item, self._fomod_path, self._flag_names_supplier
                )
            )[0]
        )
        window.saved.connect(
            lambda: self.__dependencies_tree_widget_editor.updateItem(item)
        )
        window.show_and_activate()

    @override
    def validate(self) -> None:
        if (
            self.__game_version_checkbox.isChecked()
            and not self.__game_version_entry.text().strip()
        ):
            raise SpecificValidationError(
                self.tr("Game version is checked but missing!")
            )

        if (
            self.__fomm_version_checkbox.isChecked()
            and not self.__fomm_version_entry.text().strip()
        ):
            raise SpecificValidationError(
                self.tr("FOMM version is checked but missing!")
            )

        if not any(
            [
                self.__files_tree_widget_editor.getItems(),
                self.__flags_tree_widget_editor.getItems(),
                self.__game_version_checkbox.isChecked(),
                self.__fomm_version_checkbox.isChecked(),
                self.__dependencies_tree_widget_editor.getItems(),
            ]
        ):
            raise EmptyError

    @override
    def save(self) -> CompositeDependency:
        self._item.file_dependencies = self.__files_tree_widget_editor.getItems()
        self._item.flag_dependencies = self.__flags_tree_widget_editor.getItems()

        if self.__game_version_checkbox.isChecked():
            self._item.game_dependency = VersionDependency(
                version=self.__game_version_entry.text().strip()
            )
        else:
            self._item.game_dependency = None

        if self.__fomm_version_checkbox.isChecked():
            self._item.fomm_dependency = VersionDependency(
                version=self.__fomm_version_entry.text().strip()
            )
        else:
            self._item.fomm_dependency = None

        self._item.dependencies = self.__dependencies_tree_widget_editor.getItems()

        self.saved.emit(self._item)
        return self._item

    @override
    def discard(self) -> None:
        self.__files_tree_widget_editor.setItems(self._item.file_dependencies)
        self.__flags_tree_widget_editor.setItems(self._item.flag_dependencies)

        if self._item.game_dependency is not None:
            self.__game_version_checkbox.setChecked(True)
            self.__game_version_entry.setText(self._item.game_dependency.version)
        else:
            self.__game_version_checkbox.setChecked(False)
            self.__game_version_entry.setText("")

        if self._item.fomm_dependency is not None:
            self.__fomm_version_checkbox.setChecked(True)
            self.__fomm_version_entry.setText(self._item.fomm_dependency.version)
        else:
            self.__fomm_version_checkbox.setChecked(False)
            self.__fomm_version_entry.setText("")

        self.__dependencies_tree_widget_editor.setItems(self._item.dependencies)

        self.discarded.emit()
