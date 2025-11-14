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

import time

from epics import caget, caput
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

    # Additional PVs
    _detector_acquire: str = "13IDD:userStringSeq11.PROC"
    _detector_acquire: str = "13EIG2_9M:cam1:Acquire"
    _photodiode: str = "13IDD:Photodiode"

    _start_position: float = None
    _end_position: float = None
    _exposure_time: float = None

    def __init__(self) -> None:
        super(ScanningModel, self).__init__()

    @staticmethod
    def create_error_message(msg: str) -> None:
        print(f"[Generic-Error] - {msg}")
        ErrorMessageBox(msg=msg)

    def _wait_for_collection(self) -> None:
        while not self._aborted:
            if not caget(self._detector_acquire):
                time.sleep(0.1)
            continue

        # Add delay
        time.sleep(5)

    def prepare_scan(
        self,
        start: float,
        end: float,
        exposure: float,
        step: float,
    ) -> bool:
        self.scan_is_running.emit(True)
        self._is_running = True
        self.status_message_changed.emit("Preparing")
        # self._start_position = start
        # self._end_position = end
        # self._exposure_time = exposure

        limited = False

        # TODO: Check scan limits

        return limited

    def collect(
        self,
        start: float,
        end: float,
        exposure: float,
        step: float,
    ) -> None:
        # Set the scan status to running
        self.status_message_changed.emit("Scanning")

        # Arm the detector
        time.sleep(0.5)

        self._wait_for_collection()
        self._finish_scan()

    def _finish_scan(self) -> None:
        # Reset status values
        self._aborted = False
        # Change scan running status
        self.scan_is_running.emit(False)
        self._is_running = False
        # Set finish scan message
        self.status_message_changed.emit("Finished")

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
