"""
Copyright (c) Cutleast
"""

import pytest
from pytestqt.qtbot import QtBot

from core.fomod.module_config.dependency.composite_dependency import CompositeDependency
from core.fomod_editor.exceptions import EmptyError
from tests.ui.ui_test import UiTest
from tests.utils import Utils
from ui.fomod_editor.dependency_editor.composite_dependency_editor_widget import (
    CompositeDependencyEditorWidget,
)
from ui.fomod_editor.dependency_editor.dependency_group_editor_widget import (
    DependencyGroupEditorWidget,
)
from ui.widgets.enum_radiobutton_widget import EnumRadiobuttonsWidget


class TestCompositeDependencyEditorWidget(UiTest):
    """
    Tests `ui.fomod_editor.dependency_editor.composite_dependency_editor_widget.CompositeDependencyEditorWidget`.
    """

    DEPENDENCY_GROUP_EDITOR_WIDGET: tuple[str, type[DependencyGroupEditorWidget]] = (
        "dependency_group_editor_widget",
        DependencyGroupEditorWidget,
    )
    """Identifier for accessing the private dependency_group_editor_widget field."""

    OPERATOR_SELECTOR: tuple[
        str, type[EnumRadiobuttonsWidget[CompositeDependency.Operator]]
    ] = (
        "operator_selector",
        EnumRadiobuttonsWidget[CompositeDependency.Operator],
    )
    """Identifier for accessing the private operator_selector field."""

    @pytest.fixture
    def widget(self, qtbot: QtBot) -> CompositeDependencyEditorWidget:
        """
        Fixture to create and provide a CompositeDependencyEditorWidget instance for
        tests.
        """

        widget = CompositeDependencyEditorWidget(CompositeDependency(), None, list)
        qtbot.addWidget(widget)
        return widget

    def test_initial_state(self, widget: CompositeDependencyEditorWidget) -> None:
        """
        Tests the initial state of the widget.
        """

        # given
        operator_selector: EnumRadiobuttonsWidget[CompositeDependency.Operator] = (
            Utils.get_private_field(
                widget,
                *TestCompositeDependencyEditorWidget.OPERATOR_SELECTOR,
            )
        )

        # then
        assert operator_selector.getCurrentValue() == CompositeDependency.Operator.And

        with pytest.raises(EmptyError):
            widget.validate()
