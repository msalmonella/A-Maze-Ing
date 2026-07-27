from abc import ABC, abstractmethod
import mazegen
from ..generator.models import Path


class Renderer(ABC):

    @abstractmethod
    def __call__(self, maze: mazegen.MazeGenerator, solution: Path) -> None:
        pass
