"""
Copyright (c) Cutleast
"""

from pathlib import Path
from typing import Optional

import pytest
from PySide6.QtWidgets import QLabel, QLineEdit
from pytestqt.qtbot import QtBot

from core.fomod.module_config.install_step.group import Group
from core.fomod.module_config.install_step.install_step import InstallStep
from core.fomod.module_config.plugin.plugin import Plugin
from core.fomod_editor.exceptions import (
    NameIsMissingError,
    SpecificEmptyError,
    SpecificValidationError,
)
from tests.ui.ui_test import UiTest
from tests.utils import Utils
from ui.fomod_editor.dependency_editor.composite_dependency_editor_widget import (
    CompositeDependencyEditorWidget,
)
from ui.fomod_editor.install_step_editor.install_step_editor_widget import (
    InstallStepEditorWidget,
)


class TestInstallStepEditorWidget(UiTest):
    """
    Tests `ui.fomod_editor.install_step_editor.install_step_editor_widget.InstallStepEditorWidget`.
    """

    GROUPS: tuple[str, type[list[Group]]] = "groups", list[Group]
    """Identifier for accessing the private groups field."""

    NAME_ENTRY: tuple[str, type[QLineEdit]] = "name_entry", QLineEdit
    """Identifier for accessing the private name_entry field."""

    VISIBILITY_LABEL: tuple[str, type[QLabel]] = "visibility_label", QLabel
    """Identifier for accessing the private visibility_label field."""

    VISIBILITY_EDITOR_WIDGET: tuple[str, type[CompositeDependencyEditorWidget]] = (
        "visibility_editor_widget",
        CompositeDependencyEditorWidget,
    )
    """Identifier for accessing the private visibility_editor_widget field."""

    GROUPS_TREE_WIDGET: tuple[str, type[InstallStepEditorWidget.GroupsTreeWidget]] = (
        "groups_tree_widget",
        InstallStepEditorWidget.GroupsTreeWidget,
    )
    """Identifier for accessing the private groups_tree_widget field."""

    PLUGINS_TREE_WIDGET: tuple[str, type[InstallStepEditorWidget.PluginsTreeWidget]] = (
        "plugins_tree_widget",
        InstallStepEditorWidget.PluginsTreeWidget,
    )
    """Identifier for accessing the private plugins_tree_widget field."""

    @pytest.fixture
    def widget(self, qtbot: QtBot) -> InstallStepEditorWidget:
        """
        Fixture that creates and provides an InstallStepEditorWidget instance for tests.
        """

        return self.__get_widget(qtbot)

    def __get_widget(
        self,
        qtbot: QtBot,
        install_step: Optional[InstallStep] = None,
        fomod_path: Optional[Path] = None,
    ) -> InstallStepEditorWidget:
        widget = InstallStepEditorWidget(
            install_step or InstallStep.create(), fomod_path
        )
        qtbot.addWidget(widget)
        widget.show()
        return widget

    def test_initial_state(self, widget: InstallStepEditorWidget) -> None:
        """
        Test the initial state of the widget.
        """

        # given
        groups: list[Group] = Utils.get_private_field(
            widget, *TestInstallStepEditorWidget.GROUPS
        )
        name_entry: QLineEdit = Utils.get_private_field(
            widget, *TestInstallStepEditorWidget.NAME_ENTRY
        )
        visibility_label: QLabel = Utils.get_private_field(
            widget, *TestInstallStepEditorWidget.VISIBILITY_LABEL
        )
        groups_tree_widget: InstallStepEditorWidget.GroupsTreeWidget = (
            Utils.get_private_field(
                widget, *TestInstallStepEditorWidget.GROUPS_TREE_WIDGET
            )
        )
        plugins_tree_widget: InstallStepEditorWidget.PluginsTreeWidget = (
            Utils.get_private_field(
                widget, *TestInstallStepEditorWidget.PLUGINS_TREE_WIDGET
            )
        )

        # then
        assert groups == []

        assert name_entry.text() == ""
        assert name_entry.isVisible()

        assert visibility_label.text() == "Always visible"
        assert visibility_label.isVisible()

        assert groups_tree_widget.isEnabled()
        assert groups_tree_widget.getItems() == groups

        assert not plugins_tree_widget.isEnabled()
        assert plugins_tree_widget.getItems() == []

    def test_first_group_preselected(self, qtbot: QtBot) -> None:
        """
        Tests that the first group (if any) is preselected after initialization.
        """

        # given
        install_step: InstallStep = InstallStep.create()
        group: Group = Group.create()
        group.plugins.plugins.append(Plugin.create())
        install_step.optional_file_groups.groups.append(group)
        widget: InstallStepEditorWidget = self.__get_widget(qtbot, install_step)
        # this is required as the widget creates a deepcopy
        groups: list[Group] = Utils.get_private_field(
            widget, *TestInstallStepEditorWidget.GROUPS
        )

        groups_tree_widget: InstallStepEditorWidget.GroupsTreeWidget = (
            Utils.get_private_field(
                widget, *TestInstallStepEditorWidget.GROUPS_TREE_WIDGET
            )
        )
        plugins_tree_widget: InstallStepEditorWidget.PluginsTreeWidget = (
            Utils.get_private_field(
                widget, *TestInstallStepEditorWidget.PLUGINS_TREE_WIDGET
            )
        )

        # then
        assert groups_tree_widget.getCurrentItem() is groups[0]
        assert plugins_tree_widget.isEnabled()
        assert plugins_tree_widget.getItems() == group.plugins.plugins

    def test_group_validation(
        self, widget: InstallStepEditorWidget, qtbot: QtBot
    ) -> None:
        """
        Tests the validation of the install step's groups.
        """

        # given
        name_entry: QLineEdit = Utils.get_private_field(
            widget, *TestInstallStepEditorWidget.NAME_ENTRY
        )
        groups_tree_widget: InstallStepEditorWidget.GroupsTreeWidget = (
            Utils.get_private_field(
                widget, *TestInstallStepEditorWidget.GROUPS_TREE_WIDGET
            )
        )
        plugins_tree_widget: InstallStepEditorWidget.PluginsTreeWidget = (
            Utils.get_private_field(
                widget, *TestInstallStepEditorWidget.PLUGINS_TREE_WIDGET
            )
        )

        # when/then
        with pytest.raises(NameIsMissingError):
            widget.validate()

        # when
        with qtbot.waitSignal(widget.changed):
            name_entry.setText("Test")

        # when/then
        with pytest.raises(
            SpecificEmptyError, match="At least one group must be added!"
        ):
            widget.validate()

        # when
        group: Group = Group.create()

        with qtbot.waitSignal(widget.changed):
            groups_tree_widget.addItem(group)

        # when/then
        with pytest.raises(
            SpecificValidationError, match="Every group must have at least one plugin!"
        ):
            widget.validate()

        # when
        groups_tree_widget.setCurrentItem(group)
        plugin: Plugin = Plugin.create()

        with qtbot.waitSignal(widget.changed):
            plugins_tree_widget.addItem(plugin)

        # then
        widget.validate()

        # when
        install_step: InstallStep = widget.save()

        # then
        assert install_step.name == "Test"
        assert install_step.optional_file_groups.groups == [group]
        assert group.plugins.plugins == [plugin]
