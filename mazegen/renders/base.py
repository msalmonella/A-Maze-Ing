from abc import ABC, abstractmethod
import mazegen
from ..generator.models import GridIndex


class Renderer(ABC):

    @abstractmethod
    def __call__(
        self, maze: mazegen.MazeGenerator, solution: list[GridIndex]
    ) -> None:
        pass
