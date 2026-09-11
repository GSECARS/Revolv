# SPDX-License-Identifier: MIT

from gsewidgets import FullComboBox, Label, NumericSpinBox
from qtpy.QtCore import QSize
from qtpy.QtWidgets import QFrame, QGridLayout, QHBoxLayout


class SetupView(QFrame):
    """This class is responsible for controlling the process start and stop of the application."""

    def __init__(self) -> None:
        super(SetupView, self).__init__()

        # Labels
        self._lbl_scan_type = Label("Scan Type")
        self._lbl_laser_type = Label("Laser Type")
        self._lbl_exposure = Label("Exposure (s)")
        self._lbl_start = Label("Start (μm)")
        self._lbl_end = Label("End (μm)")
        self._lbl_step_size = Label("Step Size (μm)")

        # Input fields
        self.input_exposure = NumericSpinBox(min_value=0.1, max_value=30.0, default_value=1.0, incremental_step=0.5, precision=1)
        self.input_start = NumericSpinBox(min_value=-0.1, max_value=0.0, default_value=-0.01, incremental_step=0.005, precision=4)
        self.input_end = NumericSpinBox(min_value=0.0, max_value=0.1, default_value=0.01, incremental_step=0.005, precision=4)
        self.input_step_size = NumericSpinBox(min_value=0.0003, max_value=0.05, default_value=0.002, incremental_step=0.001, precision=4)

        # Dropdowns
        self.drop_scan_type = FullComboBox(size=QSize(150, 32))
        self.drop_laser_type = FullComboBox(size=QSize(150, 32))

        # Run configuration methods
        self._configure_setup_view()
        self._layout()

    def _configure_setup_view(self) -> None:
        """Configures the setup view."""

        # Dropdown items
        self.drop_scan_type.addItems(["Step"])
        self.drop_laser_type.addItems(["Both", "Only DS", "Only US"])

    def toggle_visibility(self, state: bool) -> None:
        """Toggles the visibility of the setup view."""
        self.input_exposure.setEnabled(not state)
        self.input_start.setEnabled(not state)
        self.input_end.setEnabled(not state)
        self.input_step_size.setEnabled(not state)
        self.drop_scan_type.setEnabled(not state)
        self.drop_laser_type.setEnabled(not state)

    def _layout(self) -> None:
        """Sets up the layout of the setup view."""
        layout = QHBoxLayout()

        left_layout = QGridLayout()
        left_layout.addWidget(self._lbl_scan_type, 0, 0)
        left_layout.addWidget(self.drop_scan_type, 0, 1)
        left_layout.addWidget(self._lbl_laser_type, 1, 0)
        left_layout.addWidget(self.drop_laser_type, 1, 1)

        right_layout = QGridLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.addWidget(self._lbl_exposure, 0, 0)
        right_layout.addWidget(self.input_exposure, 0, 1)
        right_layout.addWidget(self._lbl_start, 1, 0)
        right_layout.addWidget(self.input_start, 1, 1)
        right_layout.addWidget(self._lbl_end, 2, 0)
        right_layout.addWidget(self.input_end, 2, 1)
        right_layout.addWidget(self._lbl_step_size, 3, 0)
        right_layout.addWidget(self.input_step_size, 3, 1)

        layout.addLayout(left_layout)
        layout.addLayout(right_layout)

        self.setLayout(layout)
