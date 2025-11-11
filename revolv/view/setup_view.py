#!/usr/bin/python3
# ----------------------------------------------------------------------------------
# Project: Revolv
# File: revolv/view/setup_view.py
# ----------------------------------------------------------------------------------
# Purpose:
# This file contains the SetupView class, which is responsible for the setup view
# of the Revolv application.
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

from gsewidgets import FullComboBox, Label, NumericSpinBox
from qtpy.QtCore import QSize
from qtpy.QtWidgets import QFrame, QGridLayout, QHBoxLayout


class SetupView(QFrame):
    """This class is responsible for controlling the process start and stop of the application."""

    def __init__(self) -> None:
        super(SetupView, self).__init__()

        # Labels
        self._lbl_scan_type = Label("Scan Type")
        self._lbl_laser_type = Label("Laser Type")
        self._lbl_exposure = Label("Exposure (s)")
        self._lbl_range = Label("Range (± μm)")
        self._lbl_step_size = Label("Step Size (μm)")

        # Input fields
        self.input_exposure = NumericSpinBox(min_value=0.1, max_value=1000.0, default_value=0.5, incremental_step=0.1, precision=2)
        self.input_range = NumericSpinBox(min_value=0.1, max_value=1000.0, default_value=0.5, incremental_step=0.1, precision=2)
        self.input_step_size = NumericSpinBox(min_value=0.1, max_value=1000.0, default_value=0.5, incremental_step=0.1, precision=2)

        # Dropdowns
        self.drop_scan_type = FullComboBox(size=QSize(150, 32))
        self.drop_laser_type = FullComboBox(size=QSize(150, 32))

        # Run configuration methods
        self._configure_setup_view()
        self._layout()

    def _configure_setup_view(self) -> None:
        """Configures the setup view."""

        # Dropdown items
        self.drop_scan_type.addItems(["Step", "Fly"])
        self.drop_laser_type.addItems(["Both", "Only DS", "Only US"])

    def _layout(self) -> None:
        """Sets up the layout of the setup view."""
        layout = QHBoxLayout()

        left_layout = QGridLayout()
        left_layout.addWidget(self._lbl_scan_type, 0, 0)
        left_layout.addWidget(self.drop_scan_type, 0, 1)
        left_layout.addWidget(self._lbl_laser_type, 1, 0)
        left_layout.addWidget(self.drop_laser_type, 1, 1)

        right_layout = QGridLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.addWidget(self._lbl_exposure, 0, 0)
        right_layout.addWidget(self.input_exposure, 0, 1)
        right_layout.addWidget(self._lbl_range, 1, 0)
        right_layout.addWidget(self.input_range, 1, 1)
        right_layout.addWidget(self._lbl_step_size, 2, 0)
        right_layout.addWidget(self.input_step_size, 2, 1)

        layout.addLayout(left_layout)
        layout.addLayout(right_layout)

        self.setLayout(layout)
