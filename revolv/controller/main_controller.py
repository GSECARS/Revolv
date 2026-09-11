# SPDX-License-Identifier: MIT

import sys
import time

from qtpy.QtWidgets import QApplication

from revolv.controller.scanning_controller import ScanningController
from revolv.model import MainModel, QtWorkerModel
from revolv.view import MainView


class MainController:
    """This class is responsible for controlling the main application."""

    def __init__(self) -> None:
        self._app = QApplication(sys.argv)
        self._model = MainModel()
        self._view = MainView(paths=self._model.paths)

        # Controllers
        self._scanning_controller = ScanningController(self._model, self._view)

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
            time.sleep(0.05)

        # Clear camonitor instances after exiting the loop
        for pv in self._model.epics.pvs:
            pv.moving = False
            del pv

        # Set as finished so the GUI can exit
        self._view.worker_finished = True
