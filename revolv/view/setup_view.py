# SPDX-License-Identifier: MIT

import wx
from wxutils import FlatCombo, FlatLabel, FlatPanel, FloatCtrl


class SetupView(FlatPanel):
    """This class is responsible for controlling the process start and stop of the application."""

    def __init__(self, parent) -> None:
        super(SetupView, self).__init__(parent)

        # Labels
        self._lbl_scan_type = FlatLabel(self, "Scan Type")
        self._lbl_laser_type = FlatLabel(self, "Laser Type")
        self._lbl_exposure = FlatLabel(self, "Exposure (s)")
        self._lbl_start = FlatLabel(self, "Start (μm)")
        self._lbl_end = FlatLabel(self, "End (μm)")
        self._lbl_step_size = FlatLabel(self, "Step Size (μm)")

        # Input fields
        self.input_exposure = FloatCtrl(self, minval=0.1, maxval=30.0, value=1.0, precision=1)
        self.input_start = FloatCtrl(self, minval=-0.1, maxval=0.0, value=-0.01, precision=4)
        self.input_end = FloatCtrl(self, minval=0.0, maxval=0.1, value=0.01, precision=4)
        self.input_step_size = FloatCtrl(self, minval=0.0003, maxval=0.05, value=0.002, precision=4)

        # Dropdowns
        self.drop_scan_type = FlatCombo(self, choices=["Step"], size=wx.Size(150, 32))
        self.drop_laser_type = FlatCombo(self, choices=["Both", "DS Only", "US Only"], size=wx.Size(150, 32))

        # Run configuration methods
        self._layout()

    def toggle_visibility(self, state: bool) -> None:
        """Toggles the visibility of the setup view."""
        self.input_exposure.Enable(not state)
        self.input_start.Enable(not state)
        self.input_end.Enable(not state)
        self.input_step_size.Enable(not state)
        self.drop_scan_type.Enable(not state)
        self.drop_laser_type.Enable(not state)

    def _layout(self) -> None:
        """Sets up the layout of the setup view."""
        left_layout = wx.FlexGridSizer(2, 2, 8, 8)
        left_layout.AddGrowableCol(1, 1)
        left_layout.Add(self._lbl_scan_type, 0, wx.ALIGN_CENTER_VERTICAL)
        left_layout.Add(self.drop_scan_type, 1, wx.EXPAND)
        left_layout.Add(self._lbl_laser_type, 0, wx.ALIGN_CENTER_VERTICAL)
        left_layout.Add(self.drop_laser_type, 1, wx.EXPAND)

        right_layout = wx.FlexGridSizer(4, 2, 8, 8)
        right_layout.AddGrowableCol(1, 1)
        right_layout.Add(self._lbl_exposure, 0, wx.ALIGN_CENTER_VERTICAL)
        right_layout.Add(self.input_exposure, 1, wx.EXPAND)
        right_layout.Add(self._lbl_start, 0, wx.ALIGN_CENTER_VERTICAL)
        right_layout.Add(self.input_start, 1, wx.EXPAND)
        right_layout.Add(self._lbl_end, 0, wx.ALIGN_CENTER_VERTICAL)
        right_layout.Add(self.input_end, 1, wx.EXPAND)
        right_layout.Add(self._lbl_step_size, 0, wx.ALIGN_CENTER_VERTICAL)
        right_layout.Add(self.input_step_size, 1, wx.EXPAND)

        layout = wx.BoxSizer(wx.HORIZONTAL)
        layout.Add(left_layout, 1, wx.EXPAND | wx.RIGHT, 16)
        layout.Add(right_layout, 1, wx.EXPAND)
        self.SetSizer(layout)
