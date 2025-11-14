#!/usr/bin/python3
# ----------------------------------------------------------------------------------
# Project: Revolv
# File: revolv/view/status_view.py
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

from gsewidgets import Label
from qtpy.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout


class StatusView(QFrame):
    """This class is responsible for displaying the process status."""

    def __init__(self) -> None:
        super(StatusView, self).__init__()

        # Labels
        self._lbl_status = Label(text="Idle", object_name="lbl-status")
        self._lbl_frames = Label("0/0")
        self._lbl_elapsed_time = Label("00:00:00")

        # Layout
        self._layout()

    def update_status_label(self, status_message) -> None:
        """Updates the status label."""
        self._lbl_status.setText(status_message)

    def update_frames_label(self, frames) -> None:
        """Updates the frames label."""
        self._lbl_frames.setText(frames)

    def update_elapsed_time_label(self, elapsed_time) -> None:
        """Updates the elapsed time label."""
        self._lbl_elapsed_time.setText(elapsed_time)

    def _layout(self) -> None:
        """Sets up the layout of the status view."""
        layout = QHBoxLayout()
        layout.addWidget(self._lbl_status)

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self._lbl_frames)
        vertical_layout.addWidget(self._lbl_elapsed_time)

        layout.addLayout(vertical_layout)

        self.setLayout(layout)
