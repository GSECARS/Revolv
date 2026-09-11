# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class PathModel:
    """
    Model that holds the paths for the assets directories.
    """

    _assets_path: str = field(init=False, compare=False, repr=False)
    _icon_path: str = field(init=False, compare=False, repr=False)
    _qss_path: str = field(init=False, compare=False, repr=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "_assets_path", Path(__file__).parent.parent.parent / "revolv" / "assets")
        object.__setattr__(self, "_icon_path", self._assets_path / "icons")
        object.__setattr__(self, "_qss_path", self._assets_path / "qss")

    @property
    def icon_path(self) -> str:
        return self._icon_path

    @property
    def qss_path(self) -> str:
        return self._qss_path
