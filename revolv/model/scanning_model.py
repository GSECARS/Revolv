#!/usr/bin/python3
# ----------------------------------------------------------------------------------
# Project: Revolv
# File: revolv/model/scanning_model.py
# ----------------------------------------------------------------------------------
# Purpose:
# This is the scanning model of the Revolv application. It is responsible for
# defining scanning-related functionalities.
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
