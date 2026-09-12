# SPDX-License-Identifier: MIT

import sys
from importlib.resources import as_file, files

import wx


class MainView(wx.Frame):
    """Implements the main application view."""

    def __init__(self, version: str) -> None:
        super(MainView, self).__init__(parent=None, id=wx.ID_ANY, title=f"Revolv {version}")

        self._set_icon()

    def _set_icon(self) -> None:
        """Sets the application icon."""
        if sys.platform == "win32":
            filename = "revolv.ico"
            bitmap_type = wx.BITMAP_TYPE_ICO
        else:
            filename = "revolv.png"
            bitmap_type = wx.BITMAP_TYPE_PNG

        resource = files("revolv").joinpath("assets", filename)

        with as_file(resource) as path:
            self.SetIcon(wx.Icon(str(path), bitmap_type))
