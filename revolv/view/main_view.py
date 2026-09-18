# SPDX-License-Identifier: MIT

import wx


class MainView(wx.Frame):
    """Implements the main application view."""

    def __init__(self, version: str) -> None:
        super(MainView, self).__init__(parent=None, id=wx.ID_ANY, title=f"Revolv {version}")

        self._create_menu()

    def _create_menu(self) -> None:
        menu_bar = wx.MenuBar()
        file_menu = wx.Menu()
        file_menu.Append(
            wx.ID_EXIT,
            "Quit\tCtrl+Q",
        )
        menu_bar.Append(file_menu, "&File")
        self.SetMenuBar(menu_bar)
        self.Bind(
            wx.EVT_MENU,
            lambda event: self.Close(),
            id=wx.ID_EXIT,
        )
