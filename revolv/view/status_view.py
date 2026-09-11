# SPDX-License-Identifier: MIT

from gsewidgets import Label
from qtpy.QtWidgets import QFrame, QHBoxLayout, QVBoxLayout


class StatusView(QFrame):
    """This class is responsible for displaying the process status."""

    def __init__(self) -> None:
        super(StatusView, self).__init__()

        # Labels
        self._lbl_status = Label(text="Idle", object_name="lbl-status")
        self._lbl_frames = Label("0/0")
        self._lbl_elapsed_time = Label("00:00:00")

        # Layout
        self._layout()

    def update_status_label(self, status_message) -> None:
        """Updates the status label."""
        self._lbl_status.setText(status_message)

    def update_frames_label(self, frames) -> None:
        """Updates the frames label."""
        self._lbl_frames.setText(frames)

    def update_elapsed_time_label(self, elapsed_time) -> None:
        """Updates the elapsed time label."""
        self._lbl_elapsed_time.setText(elapsed_time)

    def _layout(self) -> None:
        """Sets up the layout of the status view."""
        layout = QHBoxLayout()
        layout.addWidget(self._lbl_status)

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self._lbl_frames)
        vertical_layout.addWidget(self._lbl_elapsed_time)

        layout.addLayout(vertical_layout)

        self.setLayout(layout)
