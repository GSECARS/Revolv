# SPDX-License-Identifier: MIT

from typing import Any, Callable

from qtpy.QtCore import QThread


class QtWorkerModel(QThread):
    """This class is responsible for creating a worker thread."""

    def __init__(self, method: Callable, args: Any) -> None:
        """Initialises the qt worker model."""
        super(QtWorkerModel, self).__init__()
        self._method = method
        self._args = args

    def run(self) -> None:
        """Runs the worker thread."""
        self._method(*self._args)
