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

from epics import caget, caput, caput_many
from qtpy.QtCore import QObject, Signal

from revolv.model import EpicsConfig, LineTrajectory, MainModel
from revolv.view import MainView


class ScanningController(QObject):
    frame_changed: Signal = Signal(str)
    elapsed_time_changed: Signal = Signal(str)

    def __init__(self, model: MainModel, view: MainView) -> None:
        super(ScanningController, self).__init__()

        self._model = model
        self._view = view

        self._horiz_traj = None
        self._ds_traj = None
        self._us_traj = None
        self._start_time = None

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
        self.elapsed_time_changed.connect(self._view.status_view.update_elapsed_time_label)

        self._view.control_view.btn_collect_abort.clicked.connect(self._collect_abort_btn)

        self._model.scanning.error_message_changed.connect(self._model.scanning.create_error_message)

    def _disable_gui_while_collecting(self, state: bool) -> None:
        self._view.setup_view.toggle_visibility(state)

    def _update_elapsed_time(self) -> None:
        """Calculate and emit elapsed time."""
        if self._start_time is not None:
            elapsed = time.time() - self._start_time
            hours = int(elapsed // 3600)
            minutes = int((elapsed % 3600) // 60)
            seconds = int(elapsed % 60)
            self.elapsed_time_changed.emit(f"{hours:02d}:{minutes:02d}:{seconds:02d}")

    def _check_limits(self) -> bool:
        """Check if trajectory positions exceed motor limits."""
        # Get motor limits
        horiz_llm = caget(EpicsConfig["horizontal"].value + ".LLM")
        horiz_hlm = caget(EpicsConfig["horizontal"].value + ".HLM")

        # Check horizontal trajectory limits
        if self._horiz_traj is not None:
            horiz_min = min(self._horiz_traj.trj_array)
            horiz_max = max(self._horiz_traj.trj_array)

            if horiz_min < horiz_llm or horiz_max > horiz_hlm:
                error_msg = f"Horizontal trajectory ({horiz_min:.4f} to {horiz_max:.4f}) exceeds limits ({horiz_llm:.4f} to {horiz_hlm:.4f})"
                self._model.scanning.error_message_changed.emit(error_msg)
                return True

        # Check DS mirror limits if trajectory exists
        if self._ds_traj is not None:
            ds_llm = caget(EpicsConfig["ds_mirror"].value + ".LLM")
            ds_hlm = caget(EpicsConfig["ds_mirror"].value + ".HLM")
            ds_min = min(self._ds_traj.trj_array)
            ds_max = max(self._ds_traj.trj_array)

            if ds_min < ds_llm or ds_max > ds_hlm:
                error_msg = f"DS mirror trajectory ({ds_min:.4f} to {ds_max:.4f}) exceeds limits ({ds_llm:.4f} to {ds_hlm:.4f})"
                self._model.scanning.error_message_changed.emit(error_msg)
                return True

        # Check US mirror limits if trajectory exists
        if self._us_traj is not None:
            us_llm = caget(EpicsConfig["us_mirror"].value + ".LLM")
            us_hlm = caget(EpicsConfig["us_mirror"].value + ".HLM")
            us_min = min(self._us_traj.trj_array)
            us_max = max(self._us_traj.trj_array)

            if us_min < us_llm or us_max > us_hlm:
                error_msg = f"US mirror trajectory ({us_min:.4f} to {us_max:.4f}) exceeds limits ({us_llm:.4f} to {us_hlm:.4f})"
                self._model.scanning.error_message_changed.emit(error_msg)
                return True

        return False

    def _collect_abort_btn(self) -> None:
        if not self._model.scanning.is_running:
            exposure = self._view.setup_view.input_exposure.value()
            start = self._view.setup_view.input_start.value()
            end = self._view.setup_view.input_end.value()
            step = self._view.setup_view.input_step_size.value()

            self.collect(exposure, start, end, step)
        else:
            self.abort()

    def acquire_data(self, exposure) -> None:
        # Collect
        caput(EpicsConfig["detector_acquire"].value, 1, wait=True)
        time.sleep(exposure + 0.2)

    def _collect_step(self, exposure: float, start: float, end: float, step: float) -> None:
        if self._horiz_traj is None:
            self.abort()
            return None

        self._model.scanning.scan_is_running.emit(True)
        self._model.scanning.is_running = True
        self._model.scanning.status_message_changed.emit("Preparing")

        # Start timing
        self._start_time = time.time()

        # Check for limit violations
        limited = self._check_limits()
        if limited:
            self.abort()
            return None

        # Set exposure time
        caput(EpicsConfig["detector_exposure"].value, exposure, wait=True)

        # Start collection
        self._model.scanning.status_message_changed.emit("Scanning")

        # Number of frames
        num_frames = len(self._horiz_traj.trj_array)

        if self._ds_traj is not None and self._us_traj is None:
            current_horiz = caget(EpicsConfig["horizontal"].value)
            current_ds = caget(EpicsConfig["ds_mirror"].value)

            # Move to start positions
            caput_many(
                [EpicsConfig["horizontal"].value, EpicsConfig["ds_mirror"].value], [self._horiz_traj.trj_array[0], self._ds_traj.trj_array[0]], wait=True
            )
            time.sleep(0.2)

            # Collect first step
            self.acquire_data(exposure=exposure)

            for i in range(num_frames):
                if not self._model.scanning.aborted:
                    caput_many(
                        [EpicsConfig["horizontal"].value, EpicsConfig["ds_mirror"].value],
                        [self._horiz_traj.trj_array[i], self._ds_traj.trj_array[i]],
                        wait=True,
                    )
                    self.acquire_data(exposure=exposure)
                    self.frame_changed.emit(f"{i + 1}/{num_frames}")
                    self._update_elapsed_time()

            caput_many([EpicsConfig["horizontal"].value, EpicsConfig["ds_mirror"].value], [current_horiz, current_ds], wait=True)

        elif self._us_traj is not None and self._ds_traj is None:
            current_horiz = caget(EpicsConfig["horizontal"].value)
            current_us = caget(EpicsConfig["us_mirror"].value)

            # Move to start positions
            caput_many(
                [EpicsConfig["horizontal"].value, EpicsConfig["us_mirror"].value], [self._horiz_traj.trj_array[0], self._us_traj.trj_array[0]], wait=True
            )
            time.sleep(0.2)

            # Collect first step
            self.acquire_data(exposure=exposure)

            for i in range(num_frames):
                if not self._model.scanning.aborted:
                    caput_many(
                        [EpicsConfig["horizontal"].value, EpicsConfig["us_mirror"].value],
                        [self._horiz_traj.trj_array[i], self._us_traj.trj_array[i]],
                        wait=True,
                    )
                    self.acquire_data(exposure=exposure)
                    self.frame_changed.emit(f"{i + 1}/{num_frames}")
                    self._update_elapsed_time()

            caput_many([EpicsConfig["horizontal"].value, EpicsConfig["us_mirror"].value], [current_horiz, current_us], wait=True)
        else:
            current_horiz = caget(EpicsConfig["horizontal"].value)
            current_us = caget(EpicsConfig["us_mirror"].value)
            current_ds = caget(EpicsConfig["ds_mirror"].value)

            # Move to start positions
            caput_many(
                [EpicsConfig["horizontal"].value, EpicsConfig["us_mirror"].value, EpicsConfig["ds_mirror"].value],
                [self._horiz_traj.trj_array[0], self._us_traj.trj_array[0], self._ds_traj.trj_array[0]],
                wait=True,
            )
            time.sleep(0.2)

            # Collect first step
            self.acquire_data(exposure=exposure)

            for i in range(num_frames):
                if not self._model.scanning.aborted:
                    caput_many(
                        [EpicsConfig["horizontal"].value, EpicsConfig["us_mirror"].value, EpicsConfig["ds_mirror"].value],
                        [self._horiz_traj.trj_array[i], self._us_traj.trj_array[i], self._ds_traj.trj_array[i]],
                        wait=True,
                    )
                    self.acquire_data(exposure=exposure)
                    self.frame_changed.emit(f"{i + 1}/{num_frames}")
                    self._update_elapsed_time()

            caput_many(
                [EpicsConfig["horizontal"].value, EpicsConfig["us_mirror"].value, EpicsConfig["ds_mirror"].value],
                [current_horiz, current_us, current_ds],
                wait=True,
            )

        time.sleep(0.5)

        # Finish the scan after all steps complete
        # Reset status values
        self._model.scanning.aborted = False
        # Change scan running status
        self._model.scanning.scan_is_running.emit(False)
        self._model.scanning.is_running = False
        # Set finish scan message
        self._model.scanning.status_message_changed.emit("Finished")

    def collect(self, exposure: float, start: float, end: float, step: float) -> None:
        step_scan = threading.Thread(target=self._collect_step, args=(exposure, start, end, step))
        if not self._model.scanning.aborted:
            step_scan.start()

    def setup_trajectories(self) -> list[LineTrajectory] | None:
        start = self._view.setup_view.input_start.value()
        stop = self._view.setup_view.input_end.value()
        step = self._view.setup_view.input_step_size.value()

        laser_type = self._view.setup_view.drop_laser_type.currentText()

        horiz = caget(EpicsConfig["horizontal"].value)
        us = caget(EpicsConfig["us_mirror"].value)
        ds = caget(EpicsConfig["ds_mirror"].value)

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
        self._model.scanning.status_message_changed.emit("Aborting")
        # Reset timer
        self.elapsed_time_changed.emit("00:00:00")
