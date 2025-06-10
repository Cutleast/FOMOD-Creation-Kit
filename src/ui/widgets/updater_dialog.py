"""
Copyright (c) Cutleast
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextBrowser,
    QVBoxLayout,
)
from semantic_version import Version

from .link_button import LinkButton


class UpdaterDialog(QDialog):
    """
    Class for updater dialog.
    """

    def __init__(
        self,
        installed_version: Version,
        latest_version: Version,
        changelog: str,
        download_url: str,
    ) -> None:
        super().__init__(QApplication.activeModalWidget())

        vlayout = QVBoxLayout()
        self.setLayout(vlayout)

        title_label = QLabel(self.tr("An Update is available to download!"))
        title_label.setObjectName("h2")
        vlayout.addWidget(title_label)

        version_label = QLabel(
            self.tr("Installed version")
            + f": {installed_version}"
            + " | "
            + self.tr("Latest version")
            + f": {latest_version}"
        )
        version_label.setTextInteractionFlags(
            version_label.textInteractionFlags()
            | Qt.TextInteractionFlag.TextSelectableByMouse
        )
        version_label.setCursor(Qt.CursorShape.IBeamCursor)
        vlayout.addWidget(version_label)

        vlayout.addSpacing(15)

        changelog_label = QLabel(self.tr("What's new?"))
        changelog_label.setObjectName("h3")
        vlayout.addWidget(changelog_label)

        changelog_box = QTextBrowser()
        changelog_box.setObjectName("transparent")
        changelog_box.setOpenExternalLinks(True)
        changelog_box.setMarkdown(changelog)
        vlayout.addWidget(changelog_box, 1)

        hlayout = QHBoxLayout()
        vlayout.addLayout(hlayout)

        self.cancel_button = QPushButton(self.tr("Ignore Update"))
        self.cancel_button.clicked.connect(self.accept)
        hlayout.addWidget(self.cancel_button)

        hlayout.addStretch()

        download_button = LinkButton(
            url=download_url, display_text=self.tr("Download Update")
        )
        download_button.setDefault(True)
        download_button.clicked.connect(self.accept)
        hlayout.addWidget(download_button)

        self.show()
        self.resize(800, 500)
        self.exec()
