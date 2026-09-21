# SPDX-License-Identifier: MIT

import wx

from wxutils import FlatPanel, StatusField


class StatusView(FlatPanel):
    """Display the scan status and progress."""

    def __init__(self, parent) -> None:
        super(StatusView, self).__init__(parent)

        self._status = StatusField(self, value="Idle")
        self._frames = StatusField(self, value="0/0")
        self._elapsed_time = StatusField(self, value="00:00:00")

        # Layout
        self._layout()

    def update_status_label(self, status_message: str) -> None:
        """Updates the status label."""
        self._status.SetValue(status_message)

    def update_frames_label(self, frames: str) -> None:
        """Updates the frames label."""
        self._frames.SetValue(frames)

    def update_elapsed_time_label(self, elapsed_time: str) -> None:
        """Updates the elapsed time label."""
        self._elapsed_time.SetValue(elapsed_time)

    def _layout(self) -> None:
        """Sets up the layout of the status view."""
        details = wx.BoxSizer(wx.VERTICAL)
        details.Add(self._frames, 1, wx.EXPAND | wx.BOTTOM, 4)
        details.Add(self._elapsed_time, 1, wx.EXPAND)

        layout = wx.BoxSizer(wx.HORIZONTAL)
        layout.Add(self._status, 2, wx.EXPAND | wx.RIGHT, 8)
        layout.Add(details, 1, wx.EXPAND)

        self.SetSizer(layout)
