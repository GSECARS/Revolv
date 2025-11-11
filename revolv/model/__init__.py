#!/usr/bin/python3
# ----------------------------------------------------------------------------------
# Project: Revolv
# File: revolv/model/__init__.py
# ----------------------------------------------------------------------------------
# Purpose:
# This is the main file of the model package, and it is used to initialize the
# Revolv model.
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

from revolv.model.main_model import MainModel
from revolv.model.qt_worker_model import QtWorkerModel

__all__ = ["MainModel", "QtWorkerModel"]
