# SPDX-License-Identifier: MIT

from gsewidgets import ErrorMessageBox
from qtpy.QtCore import QObject, Signal


class ScanningModel(QObject):
    # SIGNALS
    status_message_changed: Signal = Signal(str)
    scan_is_running: Signal = Signal(bool)
    error_message_changed: Signal = Signal(str)

    # Properties
    _is_running: bool = False
    _aborted: bool = False

    def __init__(self) -> None:
        super(ScanningModel, self).__init__()

    @staticmethod
    def create_error_message(msg: str) -> None:
        print(f"[Generic-Error] - {msg}")
        ErrorMessageBox(msg=msg)

    @property
    def is_running(self) -> bool:
        return self._is_running

    @is_running.setter
    def is_running(self, value: bool) -> None:
        self._is_running = value

    @property
    def aborted(self) -> bool:
        """Returns the aborted status of the collection."""
        return self._aborted

    @aborted.setter
    def aborted(self, value: bool) -> None:
        self.status_message_changed.emit("Aborting")
        self._aborted = value
