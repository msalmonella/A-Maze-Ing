"""Abstract interface for maze generation algorithms."""

from abc import ABC, abstractmethod
from random import Random
from collections.abc import Generator
from ..models import Mandatory
from ..cell import Grid


class Algorithm(ABC):
    """Generate a maze on the given grid."""

    @abstractmethod
    def __call__(
        self, grid: Grid, config: Mandatory, rng: Random
    ) -> Generator[None]:
        pass
