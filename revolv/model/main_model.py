#!/usr/bin/python3
# ----------------------------------------------------------------------------------
# Project: Revolv
# File: revolv/model/main_model.py
# ----------------------------------------------------------------------------------
# Purpose:
# This is the main model of the Revolv GUI. It is responsible for
# setting up the main model that handles the conversion process.
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

from revolv.model.epics_model import EpicsModel


@dataclass
class MainModel:
    """This class is responsible for the main model of the application."""

    epics: EpicsModel = field(init=False, repr=False, compare=False)

    def __init__(self) -> None:
        object.__setattr__(self, "epics", EpicsModel())
