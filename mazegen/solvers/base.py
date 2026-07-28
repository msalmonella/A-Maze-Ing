from abc import ABC, abstractmethod
import mazegen
from ..models import Path


class Solver(ABC):

    @abstractmethod
    def __call__(self, maze: mazegen.MazeGenerator) -> Path:
        pass
