# SPDX-License-Identifier: MIT

from dataclasses import dataclass, field

from revolv.model.epics_model import EpicsModel
from revolv.model.path_model import PathModel
from revolv.model.scanning_model import ScanningModel


@dataclass
class MainModel:
    """This class is responsible for the main model of the application."""

    epics: EpicsModel = field(init=False, repr=False, compare=False)
    scanning: ScanningModel = field(init=False, repr=False, compare=False)
    paths: PathModel = field(init=False, repr=False, compare=False)

    def __init__(self) -> None:
        object.__setattr__(self, "epics", EpicsModel())
        object.__setattr__(self, "scanning", ScanningModel())
        object.__setattr__(self, "paths", PathModel())
