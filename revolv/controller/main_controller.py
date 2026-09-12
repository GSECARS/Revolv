# SPDX-License-Identifier: MIT

from revolv.view import MainView

__all__ = ["MainController"]


class MainController:
    """This class is responsible for controlling the main application."""

    def __init__(self, view: MainView) -> None:
        self._view = view
