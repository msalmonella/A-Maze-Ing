"""Abstract base class for grid pathfinding solvers."""

from abc import ABC, abstractmethod
from ..models import Path
from ..cell import Grid
from ..models import Mandatory


class Solver(ABC):
    """Define the interface for grid pathfinding solvers."""

    @abstractmethod
    def __call__(self, grid: Grid, config: Mandatory) -> Path:
        pass
