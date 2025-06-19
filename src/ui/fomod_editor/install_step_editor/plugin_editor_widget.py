"""
Copyright (c) Cutleast
"""

from pathlib import Path
from typing import Optional, override

import qtawesome as qta
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QFormLayout, QLineEdit, QTabWidget

from core.fomod.module_config.condition.condition_flag_list import ConditionFlagList
from core.fomod.module_config.condition.set_condition_flag import SetConditionFlag
from core.fomod.module_config.file_list import FileList
from core.fomod.module_config.image import Image
from core.fomod.module_config.plugin.plugin import Plugin
from core.fomod_editor.exceptions import (
    EmptyError,
    NameIsMissingError,
    SpecificEmptyError,
)
from core.utilities.exception_handler import ExceptionHandler
from ui.widgets.browse_edit import BrowseLineEdit
from ui.widgets.collapsible_text_edit import CollapsibleTextEdit
from ui.widgets.image_label import ImageLabel
from ui.widgets.tree_widget_editor import TreeWidgetEditor

from ..base_editor_widget import BaseEditorWidget
from ..editor_dialog import EditorDialog
from ..file_list_editor_widget import FileListEditorWidget
from ..install_step_editor.set_condition_flag_editor_widget import (
    SetConditionFlagEditorWidget,
)
from ..install_step_editor.type_descriptor_editor_widget import (
    TypeDescriptorEditorWidget,
)


class PluginEditorWidget(BaseEditorWidget[Plugin]):
    """
    Widget for editing a plugin (an entry from a group from an install step).
    """

    IMAGE_HEIGHT: int = 200
    """The height in pixels of the plugin image."""

    __image_label: ImageLabel

    __flayout: QFormLayout
    __name_entry: QLineEdit
    __description_entry: CollapsibleTextEdit
    __image_path_entry: BrowseLineEdit

    __file_list_editor_widget: FileListEditorWidget
    __condition_flags_tree_widget: TreeWidgetEditor[SetConditionFlag]
    __type_descriptor_editor_widget: TypeDescriptorEditorWidget

    def __init__(self, item: Plugin, fomod_path: Path | None = None) -> None:
        super().__init__(item, fomod_path)

        self.__name_entry.textChanged.connect(lambda _: self.changed.emit())
        self.__description_entry.textChanged.connect(self.changed.emit)
        self.__image_path_entry.textChanged.connect(lambda _: self.changed.emit())
        self.__image_path_entry.textChanged.connect(
            lambda _: self.__on_image_path_change()
        )
        self.__file_list_editor_widget.changed.connect(self.changed.emit)
        self.__condition_flags_tree_widget.changed.connect(self.changed.emit)
        self.__condition_flags_tree_widget.onAdd.connect(self.__add_condition_flag)
        self.__condition_flags_tree_widget.onEdit.connect(self.__edit_condition_flag)
        self.__type_descriptor_editor_widget.changed.connect(self.changed.emit)

        if self._item.image is not None:
            self.__image_path_entry.setText(str(self._item.image.path))

    @override
    @classmethod
    def get_display_name(cls) -> str:
        return QApplication.translate("PluginEditorWidget", "Edit plugin...")

    @override
    @classmethod
    def get_description(cls) -> str:
        return QApplication.translate(
            "PluginEditorWidget",
            "A plugin represents a selectable element within a FOMOD installer that "
            "can either set a condition flag or install files/folders when selected.",
        )

    @override
    def _init_ui(self) -> None:
        super()._init_ui()

        self.__init_header()
        self.__init_form()

        self._vlayout.addSpacing(15)

        self.__init_tab_widget()

        self.setBaseSize(1000, 800)

    def __init_header(self) -> None:
        self.__image_label = ImageLabel(
            qta.icon("mdi6.image-off-outline", color="#666666").pixmap(
                PluginEditorWidget.IMAGE_HEIGHT, PluginEditorWidget.IMAGE_HEIGHT
            ),
            round_pixmap=True,
        )
        self.__image_label.setFixedHeight(PluginEditorWidget.IMAGE_HEIGHT)
        self._vlayout.addWidget(self.__image_label)

    def __init_form(self) -> None:
        self.__flayout = QFormLayout()
        self._vlayout.addLayout(self.__flayout, stretch=0)

        self.__name_entry = QLineEdit(self._item.name)
        self.__flayout.addRow(self.tr("Name:"), self.__name_entry)

        self.__description_entry = CollapsibleTextEdit()
        self.__description_entry.setPlainText(
            self._item.description if self._item.description != self._item.name else ""
        )
        self.__description_entry.setPlaceholderText(
            self.tr("Defaults to the name above.")
        )
        self.__description_entry.setExpanded(False)
        self.__flayout.addRow(self.tr("Description:"), self.__description_entry)

        self.__image_path_entry = BrowseLineEdit()
        self.__flayout.addRow(self.tr("Image:"), self.__image_path_entry)

    def __init_tab_widget(self) -> None:
        tab_widget = QTabWidget()
        tab_widget.setObjectName("centered_tab")
        tab_widget.tabBar().setExpanding(True)
        tab_widget.tabBar().setDocumentMode(True)
        self._vlayout.addWidget(tab_widget, stretch=1)

        self.__file_list_editor_widget = FileListEditorWidget(
            self._item.files or FileList()
        )
        tab_widget.addTab(self.__file_list_editor_widget, self.tr("Files"))

        self.__condition_flags_tree_widget = TreeWidgetEditor(
            self._item.condition_flags.flags
            if self._item.condition_flags is not None
            else []
        )
        tab_widget.addTab(
            self.__condition_flags_tree_widget, self.tr("Condition Flags")
        )

        self.__type_descriptor_editor_widget = TypeDescriptorEditorWidget(
            self._item.type_descriptor, self._fomod_path
        )
        tab_widget.addTab(
            self.__type_descriptor_editor_widget, self.tr("Type Descriptor")
        )

    def __on_image_path_change(self) -> None:
        image_path: Optional[Path] = (
            Path(self.__image_path_entry.text().strip())
            if self.__image_path_entry.text().strip()
            else None
        )

        if (
            image_path is not None
            and not image_path.is_absolute()
            and self._fomod_path is not None
        ):
            image_path = self._fomod_path.parent / image_path

        if image_path is not None and image_path.is_file():
            self.__image_label.setPixmap(QPixmap(str(image_path)))
        else:
            self.__image_label.setPixmap(
                qta.icon("mdi6.image-off-outline", color="#666666").pixmap(
                    PluginEditorWidget.IMAGE_HEIGHT, PluginEditorWidget.IMAGE_HEIGHT
                )
            )

    def __add_condition_flag(self) -> None:
        item = SetConditionFlag(value="", name="")
        dialog: EditorDialog[SetConditionFlagEditorWidget] = EditorDialog(
            SetConditionFlagEditorWidget(item, self._fomod_path), validate_on_init=True
        )

        if dialog.exec() == EditorDialog.DialogCode.Accepted:
            self.__condition_flags_tree_widget.addItem(item)

    def __edit_condition_flag(self, item: SetConditionFlag) -> None:
        dialog: EditorDialog[SetConditionFlagEditorWidget] = EditorDialog(
            SetConditionFlagEditorWidget(item, self._fomod_path)
        )

        if dialog.exec() == EditorDialog.DialogCode.Accepted:
            self.__condition_flags_tree_widget.updateItem(item)

    @override
    def validate(self) -> None:
        if not self.__name_entry.text().strip():
            raise NameIsMissingError

        if all(
            [
                ExceptionHandler.raises_exception(
                    self.__file_list_editor_widget.validate, EmptyError
                ),
                len(self.__condition_flags_tree_widget.getItems()) == 0,
            ]
        ):
            raise SpecificEmptyError(
                self.tr(
                    "At least one file, folder or condition flag must be specified!"
                )
            )

        self.__type_descriptor_editor_widget.validate()

    @override
    def save(self) -> Plugin:
        self._item.name = self.__name_entry.text()
        self._item.description = (
            self.__description_entry.toPlainText() or self._item.name
        )

        if not self.__image_path_entry.text().strip():
            self._item.image = None
        else:
            self._item.image = Image(path=Path(self.__image_path_entry.text().strip()))

        if (
            file_list := self.__file_list_editor_widget.save()
        ).files or file_list.folders:
            self._item.files = file_list
        else:
            self._item.files = None

        if condition_flags := self.__condition_flags_tree_widget.getItems():
            self._item.condition_flags = ConditionFlagList(flags=condition_flags)
        else:
            self._item.condition_flags = None

        self._item.type_descriptor = self.__type_descriptor_editor_widget.save()

        self.saved.emit(self._item)
        return self._item
