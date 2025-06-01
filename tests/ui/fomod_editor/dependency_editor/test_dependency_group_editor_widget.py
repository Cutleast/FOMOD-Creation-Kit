"""
Copyright (c) Cutleast
"""

import pytest
from PySide6.QtWidgets import QCheckBox, QLineEdit
from pytestqt.qtbot import QtBot

from core.fomod.module_config.dependency.composite_dependency import CompositeDependency
from core.fomod.module_config.dependency.file_dependency import FileDependency
from core.fomod.module_config.dependency.flag_dependency import FlagDependency
from core.fomod_editor.exceptions import EmptyError, SpecificValidationError
from tests.ui.ui_test import UiTest
from tests.utils import Utils
from ui.fomod_editor.dependency_editor.dependency_group_editor_widget import (
    DependencyGroupEditorWidget,
)
from ui.widgets.tree_widget_editor import TreeWidgetEditor


class TestDependencyGroupEditorWidget(UiTest):
    """
    Tests `ui.fomod_editor.dependency_editor.dependency_group_editor_widget.DependencyGroupEditorWidget`.
    """

    FILES_TREE_WIDGET_EDITOR: tuple[str, type[TreeWidgetEditor[FileDependency]]] = (
        "files_tree_widget_editor",
        TreeWidgetEditor[FileDependency],
    )
    """Identifier for accessing the private files_tree_widget_editor field."""

    FLAGS_TREE_WIDGET_EDITOR: tuple[str, type[TreeWidgetEditor[FlagDependency]]] = (
        "flags_tree_widget_editor",
        TreeWidgetEditor[FlagDependency],
    )
    """Identifier for accessing the private flags_tree_widget_editor field."""

    GAME_VERSION_CHECKBOX: tuple[str, type[QCheckBox]] = (
        "game_version_checkbox",
        QCheckBox,
    )
    """Identifier for accessing the private game_version_checkbox field."""

    GAME_VERSION_ENTRY: tuple[str, type[QLineEdit]] = "game_version_entry", QLineEdit
    """Identifier for accessing the private game_version_entry field."""

    FOMM_VERSION_CHECKBOX: tuple[str, type[QCheckBox]] = (
        "fomm_version_checkbox",
        QCheckBox,
    )
    """Identifier for accessing the private fomm_version_checkbox field."""

    FOMM_VERSION_ENTRY: tuple[str, type[QLineEdit]] = "fomm_version_entry", QLineEdit
    """Identifier for accessing the private fomm_version_entry field."""

    DEPENDENCIES_TREE_WIDGET_EDITOR: tuple[
        str, type[TreeWidgetEditor[CompositeDependency]]
    ] = (
        "dependencies_tree_widget_editor",
        TreeWidgetEditor[CompositeDependency],
    )
    """Identifier for accessing the private dependencies_tree_widget_editor field."""

    @pytest.fixture
    def widget(self, qtbot: QtBot) -> DependencyGroupEditorWidget:
        """
        Fixture that creates and provides a DependencyGroupEditorWidget instance for tests.
        """

        dependency_group_editor_widget = DependencyGroupEditorWidget(
            CompositeDependency(), None
        )
        qtbot.addWidget(dependency_group_editor_widget)
        return dependency_group_editor_widget

    def test_initial_state(self, widget: DependencyGroupEditorWidget) -> None:
        """
        Tests the initial state of the widget.
        """

        # given
        files_tree_widget_edtior: TreeWidgetEditor[FileDependency] = (
            Utils.get_private_field(
                widget, *TestDependencyGroupEditorWidget.FILES_TREE_WIDGET_EDITOR
            )
        )
        flags_tree_widget_editor: TreeWidgetEditor[FlagDependency] = (
            Utils.get_private_field(
                widget, *TestDependencyGroupEditorWidget.FLAGS_TREE_WIDGET_EDITOR
            )
        )
        game_version_checkbox: QCheckBox = Utils.get_private_field(
            widget, *TestDependencyGroupEditorWidget.GAME_VERSION_CHECKBOX
        )
        game_version_entry: QLineEdit = Utils.get_private_field(
            widget, *TestDependencyGroupEditorWidget.GAME_VERSION_ENTRY
        )
        fomm_version_checkbox: QCheckBox = Utils.get_private_field(
            widget, *TestDependencyGroupEditorWidget.FOMM_VERSION_CHECKBOX
        )
        fomm_version_entry: QLineEdit = Utils.get_private_field(
            widget, *TestDependencyGroupEditorWidget.FOMM_VERSION_ENTRY
        )
        dependencies_tree_widget_editor: TreeWidgetEditor[CompositeDependency] = (
            Utils.get_private_field(
                widget, *TestDependencyGroupEditorWidget.DEPENDENCIES_TREE_WIDGET_EDITOR
            )
        )

        # then
        assert files_tree_widget_edtior.getItems() == []
        assert flags_tree_widget_editor.getItems() == []
        assert not game_version_checkbox.isChecked()
        assert not game_version_entry.isEnabled()
        assert game_version_entry.text() == ""
        assert not fomm_version_checkbox.isChecked()
        assert not fomm_version_entry.isEnabled()
        assert fomm_version_entry.text() == ""
        assert dependencies_tree_widget_editor.getItems() == []

        with pytest.raises(EmptyError):
            widget.validate()

    def test_validate(self, qtbot: QtBot, widget: DependencyGroupEditorWidget) -> None:
        """
        Tests the validation of the widget.
        """

        # given
        files_tree_widget_editor: TreeWidgetEditor[FileDependency] = (
            Utils.get_private_field(
                widget, *TestDependencyGroupEditorWidget.FILES_TREE_WIDGET_EDITOR
            )
        )

        flags_tree_widget_editor: TreeWidgetEditor[FlagDependency] = (
            Utils.get_private_field(
                widget, *TestDependencyGroupEditorWidget.FLAGS_TREE_WIDGET_EDITOR
            )
        )

        game_version_checkbox: QCheckBox = Utils.get_private_field(
            widget, *TestDependencyGroupEditorWidget.GAME_VERSION_CHECKBOX
        )
        game_version_entry: QLineEdit = Utils.get_private_field(
            widget, *TestDependencyGroupEditorWidget.GAME_VERSION_ENTRY
        )

        fomm_version_checkbox: QCheckBox = Utils.get_private_field(
            widget, *TestDependencyGroupEditorWidget.FOMM_VERSION_CHECKBOX
        )
        fomm_version_entry: QLineEdit = Utils.get_private_field(
            widget, *TestDependencyGroupEditorWidget.FOMM_VERSION_ENTRY
        )

        dependencies_tree_widget_editor: TreeWidgetEditor[CompositeDependency] = (
            Utils.get_private_field(
                widget, *TestDependencyGroupEditorWidget.DEPENDENCIES_TREE_WIDGET_EDITOR
            )
        )

        # when/then
        with pytest.raises(EmptyError):
            widget.validate()

        # when
        with qtbot.waitSignal(widget.changed, timeout=1000):
            game_version_checkbox.setChecked(True)

        # then
        assert game_version_entry.isEnabled()
        with pytest.raises(
            SpecificValidationError, match="Game version is checked but missing!"
        ):
            widget.validate()

        # when
        with qtbot.waitSignal(widget.changed, timeout=1000):
            game_version_entry.setText("1.0")
            fomm_version_checkbox.setChecked(True)

        # then
        assert fomm_version_entry.isEnabled()
        with pytest.raises(
            SpecificValidationError, match="FOMM version is checked but missing!"
        ):
            widget.validate()

        # when
        with qtbot.waitSignal(widget.changed, timeout=1000):
            fomm_version_entry.setText("1.0")

        # then
        widget.validate()

        # when
        with qtbot.waitSignal(widget.changed, timeout=1000):
            game_version_checkbox.setChecked(False)
            fomm_version_checkbox.setChecked(False)

        # then
        assert not game_version_entry.isEnabled()
        assert not fomm_version_entry.isEnabled()
        with pytest.raises(EmptyError):
            widget.validate()

        # when
        file_dependency = FileDependency(file="", state=FileDependency.State.Active)
        with qtbot.waitSignal(widget.changed, timeout=1000):
            files_tree_widget_editor.addItem(file_dependency)

        # then
        widget.validate()

        # when
        with qtbot.waitSignal(widget.changed, timeout=1000):
            files_tree_widget_editor.removeItem(file_dependency)

        # then
        with pytest.raises(EmptyError):
            widget.validate()

        # when
        flag_dependency = FlagDependency(flag="", value="")
        with qtbot.waitSignal(widget.changed, timeout=1000):
            flags_tree_widget_editor.addItem(flag_dependency)

        # then
        widget.validate()

        # when
        with qtbot.waitSignal(widget.changed, timeout=1000):
            flags_tree_widget_editor.removeItem(flag_dependency)

        # then
        with pytest.raises(EmptyError):
            widget.validate()

        # when
        composite_dependency = CompositeDependency()
        with qtbot.waitSignal(widget.changed, timeout=1000):
            dependencies_tree_widget_editor.addItem(composite_dependency)

        # then
        widget.validate()

        # when
        with qtbot.waitSignal(widget.changed, timeout=1000):
            dependencies_tree_widget_editor.removeItem(composite_dependency)

        # then
        with pytest.raises(EmptyError):
            widget.validate()
