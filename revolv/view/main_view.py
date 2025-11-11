#!/usr/bin/python3
# ----------------------------------------------------------------------------------
# Project: Revolv
# File: revolv/view/main_view.py
# ----------------------------------------------------------------------------------
# Purpose:
# This is the main view of the Revolv application.
# ----------------------------------------------------------------------------------
# Author: Christofanis Skordas
#
# Copyright (c) 2025 GSECARS, The University of Chicago
# Copyright (c) 2025 NSF SEES, Synchrotron Earth and Environmental Science
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------------------

from qtpy.QtGui import QCloseEvent
from qtpy.QtWidgets import QFrame, QHBoxLayout, QMainWindow, QMessageBox, QVBoxLayout

from revolv.view.control_view import ControlView
from revolv.view.status_view import StatusView


class MainView(QMainWindow):
    """This class is responsible for the main view of the application."""

    def __init__(self) -> None:
        super(MainView, self).__init__()

        # Create the views
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

    def _layout(self) -> None:
        """Layouts the main view."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.addWidget(self.status_view)
        bottom_layout.addWidget(self.control_view)

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
