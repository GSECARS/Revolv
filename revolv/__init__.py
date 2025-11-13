#!/usr/bin/python3
# ----------------------------------------------------------------------------------
# Project: Revolv
# File: revolv/__init__.py
# ----------------------------------------------------------------------------------
# Purpose:
# This is the main entry point for the Revolv application.
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

import argparse
import shutil
from importlib.metadata import version
from pathlib import Path

from pyshortcuts import make_shortcut

from revolv.controller import MainController


def make_icon() -> None:
    """Creates a desktop shortcut icon for the application."""
    print("Creating desktop shortcut...")

    # Find the path to the main script
    revolv_script = shutil.which("revolv")
    if not revolv_script:
        raise FileNotFoundError("Could not find the 'revolv' script in PATH.")

    # Get the package directory to find the icon
    package_dir = Path(__file__).parent.parent
    revolv_icon = str(package_dir / "icons" / "revolv_icon.png")

    # Create the shortcut using pyshortcuts
    make_shortcut(script=f"{revolv_script} -g", name="Revolv", icon=revolv_icon, terminal=False)


def main() -> None:
    """Main entry point for `revolv` console script."""
    parser = argparse.ArgumentParser("Revolv CLI")
    parser.add_argument("-m", "--make-icon", action="store_true", help="create desktop shortcut icon")
    parser.add_argument("-g", "--gui", action="store_true", help="launch the GUI application")

    args = parser.parse_args()

    if args.make_icon:
        make_icon()
    elif args.gui:
        MainController().run(version("revolv"))
    else:
        parser.print_help()
