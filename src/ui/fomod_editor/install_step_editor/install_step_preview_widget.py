"""
Copyright (c) Cutleast
"""

from pathlib import Path
from typing import Optional

import qtawesome as qta
from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QCheckBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)

from core.fomod.module_config.install_step.group import Group
from core.fomod.module_config.install_step.install_step import InstallStep
from core.fomod.module_config.plugin.plugin import Plugin
from core.fomod.module_config.plugin.plugin_type import PluginType
from core.utilities.path import get_joined_path_if_relative
from ui.utilities.rounded_pixmap import rounded_pixmap
from ui.utilities.tool_tip import pixmap_to_html
from ui.widgets.smooth_scroll_area import SmoothScrollArea


class InstallStepPreviewWidget(SmoothScrollArea):
    """
    Widget for displaying a single install step without the ability to edit it.
    """

    class GroupWidget(QGroupBox):
        """
        Widget for displaying a group of plugins from this install step.
        """

        IMAGE_HEIGHT: int = 256

        def __init__(self, group: Group, fomod_path: Optional[Path] = None) -> None:
            super().__init__(group.name)

            self.setObjectName("regular")

            self.__init_ui(group, fomod_path)

        def __init_ui(self, group: Group, fomod_path: Optional[Path] = None) -> None:
            flayout = QFormLayout()
            flayout.setVerticalSpacing(0)
            self.setLayout(flayout)

            flayout.addRow(self.tr("Type:"), QLabel(group.type.get_localized_name()))

            for plugin in group.plugins.plugins:
                plugin_button: QCheckBox | QRadioButton
                if group.type in (
                    Group.Type.SelectAtMostOne,
                    Group.Type.SelectExactlyOne,
                ):
                    plugin_button = QRadioButton(plugin.name)
                else:
                    plugin_button = QCheckBox(plugin.name)
                plugin_button.setChecked(
                    plugin.type_descriptor.type is not None
                    and plugin.type_descriptor.type.name
                    in [PluginType.Type.Required, PluginType.Type.Recommended]
                )
                plugin_button.setDisabled(
                    plugin.type_descriptor.type is not None
                    and plugin.type_descriptor.type.name == PluginType.Type.Required
                )
                plugin_button.setToolTip(
                    self.__create_tooltip_text_for_plugin(plugin, fomod_path)
                )
                flayout.addRow(plugin_button)

        def __create_tooltip_text_for_plugin(
            self, plugin: Plugin, fomod_path: Optional[Path] = None
        ) -> str:
            html_text: str = ""

            pixmap: QPixmap
            if (
                plugin.image is not None
                and (
                    image_path := get_joined_path_if_relative(
                        plugin.image.path,
                        fomod_path.parent if fomod_path is not None else None,
                    )
                ).is_file()
            ):
                pixmap = rounded_pixmap(
                    QPixmap(str(image_path)).scaledToHeight(
                        InstallStepPreviewWidget.GroupWidget.IMAGE_HEIGHT,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                )
            else:
                pixmap = qta.icon("mdi6.image-off-outline", color="#666666").pixmap(
                    InstallStepPreviewWidget.GroupWidget.IMAGE_HEIGHT,
                    InstallStepPreviewWidget.GroupWidget.IMAGE_HEIGHT,
                )

            html_text: str = f"""
<center>{pixmap_to_html(pixmap)}</center>
<br>
{plugin.description}
"""

            return html_text

    onEdit = Signal(InstallStep)
    """
    Signal emitted when the user clicks the edit button.

    Args:
        InstallStep: The install step to edit.
    """

    __item: InstallStep
    __fomod_path: Optional[Path]

    __vlayout: QVBoxLayout

    __title_label: QLabel
    __edit_button: QPushButton

    __visible_when_label: QLabel
    __visibility_label: QLabel

    __groups_layout: QVBoxLayout

    def __init__(
        self,
        initial_item: Optional[InstallStep] = None,
        fomod_path: Optional[Path] = None,
        show_edit_button: bool = True,
    ) -> None:
        """
        Args:
            initial_item (Optional[InstallStep], optional):
                Initial item to display. Defaults to None.
            fomod_path (Optional[Path], optional):
                Path to the FOMOD, if any. Used for display of images. Defaults to None.
            show_edit_button (bool, optional):
                Whether to show an edit button at the top right corner. Defaults to True.
        """

        super().__init__()

        self.__fomod_path = fomod_path

        self.__init_ui()

        if initial_item is not None:
            self.set_item(initial_item)

        self.__edit_button.clicked.connect(lambda: self.onEdit.emit(self.__item))
        self.__edit_button.setVisible(show_edit_button)
        self.__edit_button.setEnabled(initial_item is not None)

    def __init_ui(self) -> None:
        scroll_widget = QWidget()
        scroll_widget.setObjectName("transparent")
        self.setWidget(scroll_widget)

        self.__vlayout = QVBoxLayout()
        self.__vlayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll_widget.setLayout(self.__vlayout)

        self.__init_header()
        self.__init_visibility_label()
        self.__init_groups_layout()

        self.setMinimumWidth(610)

    def __init_header(self) -> None:
        hlayout = QHBoxLayout()
        self.__vlayout.addLayout(hlayout)

        self.__title_label = QLabel()
        self.__title_label.setObjectName("h3")
        self.__title_label.setWordWrap(True)
        hlayout.addWidget(self.__title_label, stretch=1)

        self.__edit_button = QPushButton(
            qta.icon("mdi6.pencil", color=self.palette().text().color()), ""
        )
        self.__edit_button.setIconSize(QSize(32, 32))
        self.__edit_button.setToolTip(self.tr("Edit install step..."))
        hlayout.addWidget(self.__edit_button)

    def __init_visibility_label(self) -> None:
        hlayout = QHBoxLayout()
        self.__vlayout.addLayout(hlayout)

        self.__visible_when_label = QLabel(self.tr("Visible when:"))
        hlayout.addWidget(self.__visible_when_label)

        self.__visibility_label = QLabel()
        hlayout.addWidget(self.__visibility_label)

    def __init_groups_layout(self) -> None:
        self.__groups_layout = QVBoxLayout()
        self.__groups_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.__vlayout.addLayout(self.__groups_layout)

    def set_item(self, item: InstallStep) -> None:
        self.__item = item

        self.__title_label.setText(item.name)
        self.__visible_when_label.setVisible(item.visible is not None)
        self.__visibility_label.setText(
            str(item.visible.dependencies)
            if item.visible is not None
            else self.tr("Always visible")
        )
        self.__visibility_label.setVisible(item.visible is not None)

        while self.__groups_layout.count():
            self.__groups_layout.takeAt(0).widget().deleteLater()

        for group in item.optional_file_groups.groups:
            self.__groups_layout.addWidget(
                InstallStepPreviewWidget.GroupWidget(group, self.__fomod_path)
            )

        self.__edit_button.setEnabled(True)
