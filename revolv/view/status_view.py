#!/usr/bin/python3
# ----------------------------------------------------------------------------------
# Project: Revolv
# File: revolv/vkiew/status_view.py
# ----------------------------------------------------------------------------------
# Purpose:
# This file contains the StatusView class, which is responsible for displaying
# the process status in the Revolv application.
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

from qtpy.QtCore import Signal
from qtpy.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout


class StatusView(QFrame):
    """This class is responsible for displaying the process status."""

    update_status = Signal(str)
    update_frames = Signal(str)
    update_elapsed_time = Signal(str)

    def __init__(self) -> None:
        super(StatusView, self).__init__()

        # Labels
        self.lbl_status = QLabel("Idle")
        self.lbl_frames = QLabel("Frames: 0/0")
        self.lbl_elapsed_time = QLabel("Elapsed Time: 00:00:00")

        # Connect signals to slots
        self.update_status.connect(self._update_status_label)
        self.update_frames.connect(self._update_frames_label)
        self.update_elapsed_time.connect(self._update_elapsed_time_label)

        # Layout
        self._layout()

    def _update_status_label(self) -> None:
        """Updates the status label."""
        self.lbl_status.setText(self.update_status)

    def _update_frames_label(self) -> None:
        """Updates the frames label."""
        self.lbl_frames.setText(self.update_frames)

    def _update_elapsed_time_label(self) -> None:
        """Updates the elapsed time label."""
        self.lbl_elapsed_time.setText(self.update_elapsed_time)

    def _layout(self) -> None:
        """Sets up the layout of the status view."""
        layout = QHBoxLayout()
        layout.addWidget(self.lbl_status)

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.lbl_frames)
        vertical_layout.addWidget(self.lbl_elapsed_time)

        layout.addLayout(vertical_layout)

        self.setLayout(layout)
