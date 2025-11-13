#!/usr/bin/python3
# ----------------------------------------------------------------------------------
# Project: Revolv
# File: revolv/model/epics_model.py
# ----------------------------------------------------------------------------------
# Purpose:
# This is the EPICS model of the Revolv application. It is responsible for defining
# EPICS-related functionalities.
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

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from epics import pv
from gsewidgets import ErrorMessageBox

from revolv.model.pv_model import DoubleValuePV, PVModel, StringValuePV


class EpicsConnectionError(Exception):
    """No epics connection exception."""

    def __init__(self, message) -> None:
        super(EpicsConnectionError, self).__init__(message)
        self._message = message

    @property
    def message(self) -> str:
        ErrorMessageBox(msg=self._message)
        return f"[Epics-Connection-Error] - {self._message}"


class EpicsConfig(Enum):
    """Empty Enum to be populated with PVs"""

    ds_mirror = ""
    us_mirror = ""
    horizontal = ""
    stop_pvs = ["13IDD_Auto1:allstop.VAL", "13IDD:allstop.VAL"]


@dataclass(frozen=False)
class EpicsModel:
    """Base epics model, used for testing the connection with all PVs given."""

    ds_mirror: DoubleValuePV = field(init=False, repr=False, compare=False)
    us_mirror: DoubleValuePV = field(init=False, repr=False, compare=False)
    horizontal: DoubleValuePV = field(init=False, repr=False, compare=False)

    pvs: list[PVModel] = field(init=False, repr=False, compare=False, default_factory=lambda: [])
    _connected: bool = field(init=False, compare=False, repr=False, default=False)

    # def __post_init__(self) -> None:
    #     self._set_stages()

    def connect(self) -> None:
        """Check and set the connection status of all PVs included in the EpicsConfig."""
        if not len(EpicsConfig):
            return None

        for name, member in EpicsConfig.__members__.items():
            if not len(member.value) > 2:
                value = member.value[0]
            else:
                value = member.value

            try:
                pv_check = pv.get_pv(value, connect=True)
                if not pv_check.connected:
                    raise EpicsConnectionError(f"Could not connect {name} ({value})")
            except EpicsConnectionError:
                return None

        object.__setattr__(self, "_connected", True)

    def _add_pv(
        self,
        pv_name: str,
        movable: bool,
        limited: bool,
        rbv_extension: bool,
        monitor: Optional[bool] = False,
        as_string: Optional[bool] = False,
    ) -> None:
        name = pv_name
        if "_" in name:
            name.replace("_", " ")

        if as_string:
            pv_type = StringValuePV
        else:
            pv_type = DoubleValuePV

        object.__setattr__(
            self,
            pv_name,
            pv_type(
                name=name,
                pv=EpicsConfig[pv_name].value,
                movable=movable,
                limited=limited,
                rbv_extension=rbv_extension,
                monitor=monitor,
            ),
        )
        self.pvs.append(getattr(self, pv_name))

    def _set_stages(self) -> None:
        # Stages
        self._add_pv(
            pv_name="ds_mirror",
            movable=True,
            limited=True,
            rbv_extension=True,
            monitor=True,
        )
        self._add_pv(
            pv_name="us_mirror",
            movable=True,
            limited=True,
            rbv_extension=True,
            monitor=True,
        )
        self._add_pv(
            pv_name="horizontal",
            movable=True,
            limited=True,
            rbv_extension=True,
            monitor=True,
        )

    @property
    def connected(self) -> bool:
        return self._connected
