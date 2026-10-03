# SPDX-License-Identifier: MIT

import wx
from wxutils import FlatButton, FlatPanel, get_theme


class ControlView(FlatPanel):
    """This class is responsible for controlling the process start and stop of the application."""

    def __init__(self, parent) -> None:
        super(ControlView, self).__init__(parent)

        # Button
        self.btn_collect_abort = FlatButton(self, "Collect", size=(200, 70))
        self.toggle_collect_abort_button(False)

        # Layout
        self._layout()

    def _layout(self) -> None:
        """Sets up the layout of the control view."""
        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(self.btn_collect_abort, 0, wx.EXPAND)
        self.SetSizer(layout)

    def toggle_collect_abort_button(self, state: bool) -> None:
        """Toggles the style to account for collect and abort."""
        theme = get_theme()
        if not state:
            self.btn_collect_abort.SetLabel("Collect")
            self.btn_collect_abort.SetColorScheme((theme.yellow, theme.bright_yellow, theme.bright_yellow, theme.background, theme.background))
        else:
            self.btn_collect_abort.SetLabel("Abort")
            self.btn_collect_abort.SetColorScheme((theme.red, theme.bright_red, theme.bright_red, theme.foreground, theme.foreground))
