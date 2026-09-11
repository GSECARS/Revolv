# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from typing import Sequence

import numpy as np


@dataclass
class LineTrajectory:
    """Generates points along a straight line in 1D, 2D, or 3D space."""

    start: Sequence[float]
    stop: Sequence[float]
    step: float
    decimal_places: int = field(default=3)

    _start: np.ndarray = field(init=False, repr=False)
    _stop: np.ndarray = field(init=False, repr=False)
    _num_points: int = field(init=False, repr=False)
    _trj_array: np.ndarray = field(init=False, repr=False)

    def __post_init__(self):
        """Converts start and stop to numpy arrays and validates inputs."""
        # Validate step size
        if self.step <= 0:
            raise ValueError(f"Step size must be positive, got {self.step}.")

        # Validate decimal places
        if self.decimal_places < 0:
            raise ValueError(f"Decimal places must be non-negative, got {self.decimal_places}.")

        # Convert to numpy arrays
        self._start = np.atleast_1d(np.array(self.start, dtype=float))
        self._stop = np.atleast_1d(np.array(self.stop, dtype=float))

        # Validate dimensions
        if self._start.shape != self._stop.shape:
            raise ValueError("Start and stop points must have the same dimensions.")

        # Round limits to specified decimal places using ceil
        rounded_start = np.ceil(self._start * (10**self.decimal_places)) / (10**self.decimal_places)
        rounded_stop = np.ceil(self._stop * (10**self.decimal_places)) / (10**self.decimal_places)

        # Calculate distance and number of points
        distance = np.linalg.norm(rounded_stop - rounded_start)
        if distance == 0:
            # When start equals stop (after rounding), return single point
            self._num_points = 1
        else:
            # Calculate number of points: 1 + (distance / step), using round to handle floating point precision
            self._num_points = int(round(1 + distance / self.step))

    def _generate(self) -> None:
        """Generates points along the line from start to stop."""
        if self._start.shape[0] == 1:
            # 1D case
            self._trj_array = np.linspace(self._start[0], self._stop[0], self._num_points).reshape(-1, 1)
        else:
            # 2D or 3D
            self._trj_array = np.column_stack([np.linspace(self._start[i], self._stop[i], self._num_points) for i in range(self._start.shape[0])])

    @property
    def trj_array(self) -> np.ndarray:
        """Returns the generated trajectory array."""
        if not hasattr(self, "_trj_array"):
            self._generate()
        return np.round(self._trj_array, self.decimal_places)
