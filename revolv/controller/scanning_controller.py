#!/usr/bin/python3
# ----------------------------------------------------------------------------------
# Project: Revolv
# File: revolv/controller/scanning_controller.py
# ----------------------------------------------------------------------------------
# Purpose:
# This is the scanning controller for the Revolv application.
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

import threading
import time

from epics import caget, caput
from qtpy.QtCore import QObject, Signal

from revolv.model import LineTrajectory, MainModel
from revolv.view import MainView


class ScanningController(QObject):
    frame_changed: Signal = Signal(str)

    def __init__(self, model: MainModel, view: MainView) -> None:
        super(ScanningController, self).__init__()

        self._model = model
        self._view = view

        self._horiz_traj = None
        self._ds_traj = None
        self._us_traj = None

        self.setup_trajectories()
        self._connect_methods()

    def _connect_methods(self) -> None:
        self._model.scanning.status_message_changed.connect(self._view.status_view.update_status_label)
        self._model.scanning.scan_is_running.connect(self._view.control_view.toggle_collect_abort_button)
        self._model.scanning.scan_is_running.connect(self._disable_gui_while_collecting)
        self._view.setup_view.input_start.valueChanged.connect(self.setup_trajectories)
        self._view.setup_view.input_end.valueChanged.connect(self.setup_trajectories)
        self._view.setup_view.input_step_size.valueChanged.connect(self.setup_trajectories)
        self._view.setup_view.drop_laser_type.currentIndexChanged.connect(self.laser_type_changed)
        self.frame_changed.connect(self._view.status_view.update_frames_label)

        self._view.control_view.btn_collect_abort.clicked.connect(self._collect_abort_btn)

        self._model.scanning.error_message_changed.connect(self._model.scanning.create_error_message)

    def _disable_gui_while_collecting(self, state: bool) -> None:
        self._view.setup_view.toggle_visibility(state)

    def _collect_abort_btn(self) -> None:
        if self._view.control_view.btn_collect_abort.text() == "Collect":
            exposure = self._view.setup_view.input_exposure.value()
            start = self._view.setup_view.input_start.value()
            end = self._view.setup_view.input_end.value()
            step = self._view.setup_view.input_step_size.value()

            self.collect(exposure, start, end, step)
        else:
            self.abort()

    def _collect_step(self, exposure: float, start: float, end: float, step: float) -> None:
        if self._horiz_traj is None:
            self.abort()
            return None

        limited = self._model.scanning.prepare_scan(start=start, end=end, exposure=exposure, step=step)
        if limited:
            self.abort()
            return None

        # Start collection
        self._model.scanning.collect(start, end, exposure, step)

        # Number of frames
        num_frames = len(self._horiz_traj.trj_array)

        if self._ds_traj is not None and self._us_traj is None:
            for i in len(self._horiz_traj.trj_array):
                horiz_pos = self._horiz_traj.trj_array[i]
                ds_pos = self._ds_traj.trj_array[i]
                print(f"Moving horiz to {horiz_pos}, ds to {ds_pos}")
                time.sleep(exposure)
                self.frame_changed.emit(f"{i + 1}/{num_frames}")

        elif self._us_traj is not None and self._ds_traj is None:
            for i in len(self._horiz_traj.trj_array):
                horiz_pos = self._horiz_traj.trj_array[i]
                us_pos = self._us_traj.trj_array[i]
                print(f"Moving horiz to {horiz_pos}, us to {us_pos}")
                time.sleep(exposure)
                self.frame_changed.emit(f"{i + 1}/{num_frames}")
        else:
            for i in len(self._horiz_traj.trj_array):
                horiz_pos = self._horiz_traj.trj_array[i]
                us_pos = self._us_traj.trj_array[i]
                ds_pos = self._ds_traj.trj_array[i]
                print(f"Moving horiz to {horiz_pos}, us to {us_pos}, ds to {ds_pos}")
                time.sleep(exposure)
                self.frame_changed.emit(f"{i + 1}/{num_frames}")

        time.sleep(0.5)

    def collect(self, exposure: float, start: float, end: float, step: float) -> None:
        step_scan = threading.Thread(target=self._collect_step, args=(exposure, start, end, step))
        if not self._model.scanning.aborted:
            step_scan.start()

    def setup_trajectories(self) -> list[LineTrajectory] | None:
        start = self._view.setup_view.input_start.value()
        stop = self._view.setup_view.input_end.value()
        step = self._view.setup_view.input_step_size.value()

        laser_type = self._view.setup_view.drop_laser_type.currentText()

        # TODO: Update with real positions
        horiz = -1.5
        us = 0.0
        ds = 0.0

        if start is None or stop is None or step is None:
            return

        self._horiz_traj = LineTrajectory(start=[horiz - start], stop=[horiz + stop], step=step, decimal_places=4)

        if laser_type == "Both":
            self._ds_traj = LineTrajectory(start=[ds - start], stop=[ds + stop], step=step, decimal_places=4)
            self._us_traj = LineTrajectory(start=[us - start], stop=[us + stop], step=step, decimal_places=4)
        elif laser_type == "Only DS":
            self._ds_traj = LineTrajectory(start=[ds - start], stop=[ds + stop], step=step, decimal_places=4)
            self._us_traj = None
        else:
            self._us_traj = LineTrajectory(start=[us - start], stop=[us + stop], step=step, decimal_places=4)
            self._ds_traj = None

        self._view.status_view.update_frames_label(f"0/{len(self._horiz_traj.trj_array)}")

    def laser_type_changed(self) -> None:
        self._horiz_traj = None
        self._ds_traj = None
        self._us_traj = None
        self.setup_trajectories()

    def abort(self) -> None:
        self._model.scanning.aborted = True
        self._model.scanning.status_message_changed.emit("Aborted")
