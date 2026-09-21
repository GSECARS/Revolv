# SPDX-License-Identifier: MIT

import wx
from wxutils import FlatPanel

from revolv.view.status_view import StatusView


class MainView(wx.Frame):
    """Implements the main application view."""

    def __init__(self, version: str, with_inspect: bool = False) -> None:
        super(MainView, self).__init__(parent=None, id=wx.ID_ANY, title=f"Revolv {version}")

        self.with_inspect = with_inspect

        self._create_menu()

        # Panels
        self._flat_panel = FlatPanel(self)
        self.status_view = StatusView(self._flat_panel)

        # Layout
        self._layout()

    def _create_menu(self) -> None:
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        file_menu.Append(wx.ID_EXIT, "Quit\tCtrl+Q")
        menu_bar.Append(file_menu, "&File")
        self.SetMenuBar(menu_bar)
        self.Bind(wx.EVT_MENU, lambda event: self.Close(), id=wx.ID_EXIT)

        if self.with_inspect:
            inspect_item = file_menu.Append(wx.ID_ANY, "Show wxPython Inspector\tCtrl+I", "Debug wxPython App")
            self.Bind(wx.EVT_MENU, self._show_inspection_tool, inspect_item)

    @staticmethod
    def _show_inspection_tool(event=None) -> None:
        """Shows the wx inspection tool."""
        wx.GetApp().ShowInspectionTool().Show()

    def _layout(self) -> None:
        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(self.status_view, 0, wx.EXPAND | wx.ALL, 12)
        self._flat_panel.SetSizer(layout)

        self.SetClientSize((700, 400))
        self.Centre()
