#!/usr/bin/python3
# ----------------------------------------------------------------------------------
# Project: Revolv
# File: revolv/controller/main_controller.py
# ----------------------------------------------------------------------------------
# Purpose:
# This is the main controller for the Revolv application.
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

import sys
import time

from qtpy.QtWidgets import QApplication

from revolv.model import MainModel, QtWorkerModel
from revolv.view import MainView


class MainController:
    """This class is responsible for controlling the main application."""

    def __init__(self) -> None:
        self._app = QApplication(sys.argv)
        self._view = MainView()
        self._model = MainModel()

        # Initialize the Qt worker model
        self._worker_model = QtWorkerModel(self._worker_methods, ())
        self._worker_model.start()

    def run(self, version: str) -> None:
        """Runs the main application."""
        # Display the main view
        self._view.display_window(version)

        # Start the Qt app and return the status code
        sys.exit(self._app.exec())

    def _worker_methods(self) -> None:
        """This method is responsible for running the worker methods."""

        # Run the conversion process
        while not self._view.terminated:
            print("Worker is running...")
            time.sleep(0.05)

        # Clear camonitor instances after exiting the loop
        for pv in self._model.epics.pvs:
            pv.moving = False
            del pv

        # Set as finished so the GUI can exit
        self._view.worker_finished = True
