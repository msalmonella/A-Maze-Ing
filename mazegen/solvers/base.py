from abc import ABC, abstractmethod
import mazegen
from ..generator.models import GridIndex


class Solver(ABC):

    @abstractmethod
    def __call__(self, maze: mazegen.MazeGenerator) -> list[GridIndex]:
        pass
