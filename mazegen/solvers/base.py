from abc import ABC, abstractmethod
from ..models import Path
from ..cell import Grid
from ..models import Mandatory


class Solver(ABC):

    @abstractmethod
    def __call__(self, grid: Grid, config: Mandatory) -> Path:
        pass
