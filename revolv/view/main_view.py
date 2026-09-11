# SPDX-License-Identifier: MIT

from pathlib import Path

from qtpy.QtGui import QCloseEvent, QIcon
from qtpy.QtWidgets import QFrame, QHBoxLayout, QMainWindow, QMessageBox, QVBoxLayout

from revolv.model.path_model import PathModel
from revolv.view.control_view import ControlView
from revolv.view.setup_view import SetupView
from revolv.view.status_view import StatusView


class MainView(QMainWindow):
    """This class is responsible for the main view of the application."""

    def __init__(self, paths: PathModel) -> None:
        super(MainView, self).__init__()

        # Store paths
        self._paths = paths

        # Create the views
        self.setup_view = SetupView()
        self.control_view = ControlView()
        self.status_view = StatusView()

        # Helper variables
        self._terminated = False
        self.worker_finished = False

        # Run the configuration methdods
        self._configure_view()
        self._layout()

    def _configure_view(self) -> None:
        """Configures the main view."""
        # Main frame
        self._main_frame = QFrame()
        self.setCentralWidget(self._main_frame)

        # Set window size
        self.setFixedSize(430, 200)

        # Set the icon
        self.setWindowIcon(QIcon(str(Path(self._paths.icon_path) / "revolv.png")))

        # Load qss
        self.setStyleSheet(open(str(Path(self._paths.qss_path) / "main.qss"), "r").read())

    def _layout(self) -> None:
        """Layouts the main view."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.addWidget(self.status_view)
        bottom_layout.addWidget(self.control_view)

        layout.addWidget(self.setup_view)
        layout.addLayout(bottom_layout)

        self._main_frame.setLayout(layout)

    def display_window(self, version: str = "") -> None:
        """Displays the main window."""
        # Set window title
        self.setWindowTitle(f"Revolv {version}")

        # Show the main window
        self.showNormal()

    def closeEvent(self, event: QCloseEvent) -> None:
        """Creates a message box for exit confirmation if closeEvent is triggered."""
        _msg_question = QMessageBox.question(self, "Exit confirmation", "Are you sure you want to close the application?")

        if _msg_question == QMessageBox.Yes:
            self._terminated = True

            while not self.worker_finished:
                continue

            event.accept()
        else:
            event.ignore()

    @property
    def terminated(self) -> bool:
        return self._terminated
