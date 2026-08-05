from abc import ABC, abstractmethod
import mazegen
from ..models import Path
from enum import StrEnum


class Colors(StrEnum):
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"

    RESET = "\033[0m"


class Renderer(ABC):

    @abstractmethod
    def __call__(self, maze: mazegen.MazeGenerator, solution: Path) -> None:
        pass
