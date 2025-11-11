#!/usr/bin/python3
# ----------------------------------------------------------------------------------
# Project: Revolv
# File: revolv/view/control_view.py
# ----------------------------------------------------------------------------------
# Purpose:
# This file contains the ControlView class, which is responsible for starting and
# stopping the process in the Revolv application.
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

from qtpy.QtWidgets import QFrame, QPushButton, QVBoxLayout


class ControlView(QFrame):
    """This class is responsible for controlling the process start and stop of the application."""

    def __init__(self) -> None:
        super(ControlView, self).__init__()

        # Button
        self.btn_collect_abort = QPushButton("Collect")

        # Layout
        self._layout()

    def _layout(self) -> None:
        """Sets up the layout of the control view."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.btn_collect_abort)
        self.setLayout(layout)
